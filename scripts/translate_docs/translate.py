#!/usr/bin/env python3
import json
import logging
import os
import re
import sys

import boto3
from botocore.config import Config
from reretry import retry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LANGUAGES = [
    "de-DE",  # German (Germany)
    "es-ES",  # Spanish (Spain)
    "fr-FR",  # French (France)
    "it-IT",  # Italian (Italy)
    "ja-JP",  # Japanese (Japan)
    "ko-KR",  # Korean (Korea)
    "ms-MY",  # Malay (Malaysia)
    "nb-NO",  # Norwegian Bokmål (Norway)
    "th-TH",  # Thai (Thailand)
    "vi-VN",  # Vietnamese (Vietnam)
    "zh-CN",  # Chinese (Simplified, China)
    "zh-TW",  # Chinese (Traditional, Taiwan)
    "pl-PL",  # Polish (Poland)
]


def check_env_vars():
    """Check if required environment variables are set. Exit immediately if any are missing."""
    missing = []
    for key in ("AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
        if not os.environ.get(key):
            missing.append(key)
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        sys.exit(1)


def get_model_id(model: str) -> str:
    """
    Return the cross-region inference model ID for the specified model.
    """
    REGION_PREFIX = "us"
    base_model_ids = {
        "haiku-3.5": "anthropic.claude-3-5-haiku-20241022-v1:0",
    }
    region = os.environ.get("AWS_REGION", "")
    if region not in {"us-east-1", "us-west-2"}:
        logger.warning("Region %s is not supported; defaulting to us-east-1", region)
        region = "us-east-1"

    base_model_id = base_model_ids.get(model)
    if not base_model_id:
        raise ValueError(f"Unsupported model: {model}")
    model_id = f"{REGION_PREFIX}.{base_model_id}"
    logger.info(
        "Using cross-region model ID: %s for model '%s' in region '%s'",
        model_id,
        model,
        region,
    )
    return model_id


def split_by_h2(text: str) -> list[str]:
    """
    Split markdown text by h2 headings (##) only.
    Returns a list of sections, each starting with ## if it's a heading section.
    """
    # Split by lines starting with ##
    sections = re.split(r"\n(?=## )", text)
    return [section.strip() for section in sections if section.strip()]


@retry(Exception, tries=5, delay=2, backoff=2)
def translate_text(text: str, target_lang: str) -> str:
    """
    Translation function using the AWS Bedrock Converse API.
    """
    logger.info("Starting translation for target language: %s", target_lang)
    region = os.environ.get("AWS_REGION")
    model = "haiku-3.5"
    model_id = get_model_id(model)

    # ## 見出しで分割
    text_sections = split_by_h2(text)

    system_prompt = {
        "text": (
            f"You are a professional translator. Translate the following text into {target_lang}. "
            "For example, if the target language is it-IT, translate into standard Italian as used in Italy. "
            "CRITICAL REQUIREMENTS:\n"
            "1. DO NOT translate:\n"
            "   - Personal names (leave them exactly as is)\n"
            "   - URLs and links\n"
            "   - Code blocks and commands\n"
            "   - Technical terms in backticks\n"
            "2. Keep ALL markdown formatting exactly as is\n"
            "3. Keep the exact same structure and layout\n"
            "4. Translate naturally while maintaining technical accuracy\n"
        )
    }

    complete_translation = []
    for i, section in enumerate(text_sections):
        logger.info(f"Translating section {i+1}/{len(text_sections)}")

        user_message = {"role": "user", "content": [{"text": section}]}

        payload = {
            "modelId": model_id,
            "inferenceConfig": {
                "maxTokens": 4096,
                "temperature": 0.7,
                "topP": 0.95,
            },
            "system": [system_prompt],
            "messages": [user_message],
            "additionalModelRequestFields": {},
        }

        client = boto3.client(
            "bedrock-runtime", region_name=region, config=Config(read_timeout=10000)
        )

        response = client.converse(**payload)

        if "output" in response and "message" in response["output"]:
            content_list = response["output"]["message"].get("content", [])
            if content_list and "text" in content_list[0]:
                translated_section = content_list[0]["text"].strip()
                complete_translation.append(translated_section)
            else:
                raise Exception(f"No text found in response for section {i+1}")
        else:
            raise Exception(f"Invalid response format for section {i+1}")

    # Convert list of translated sections to a single string
    final_translation = "\n\n".join(complete_translation)

    logger.info("Translation completed for target language: %s", target_lang)
    return final_translation


def update_links(
    content: str, lang_code: str, output_file: str, is_root: bool = False
) -> str:
    """
    Analyze and update links in the content for the specified language.
    - For local Markdown files (.md), add _<lang> before the file extension.
    - If the link already ends with _<lang>, do not change it.
    - Do not change absolute URLs (http://, https://).

    Additionally, for the root README translation (is_root=True):
    - If the original link starts with "./docs/..." or "docs/...", remove the "docs/" part
        to make it a relative path from the output file (docs/README_<lang>.md).
    """
    # Update Markdown (.md) links.
    md_pattern = re.compile(r"(\[[^\]]*\]\()([^)\s]+\.md)(\))", re.IGNORECASE)

    def replace_md(match):
        prefix, link, suffix = match.groups()
        if re.match(r"https?://", link):
            return match.group(0)
        if re.search(rf"_{lang_code}\.md$", link):
            return match.group(0)
        if is_root:
            new_link = re.sub(r"^(?:\./)?(?:docs/)?", "", link)
            new_link = "./" + new_link
            new_link = re.sub(r"(?i)(\.md)$", f"_{lang_code}\\1", new_link)
            return f"{prefix}{new_link}{suffix}"
        else:
            new_link = re.sub(r"(?i)(\.md)$", f"_{lang_code}\\1", link)
            return f"{prefix}{new_link}{suffix}"

    content = md_pattern.sub(replace_md, content)

    # Update image links (.png, .jpg, .jpeg, .gif) for root README:
    # e.g.: ![](./docs/imgs/bot_creation.png) → ![](./imgs/bot_creation.png)
    img_pattern = re.compile(
        r"(!\[[^\]]*\]\()([^)\s]+\.(?:png|jpg|jpeg|gif))(\))", re.IGNORECASE
    )

    def replace_img(match):
        prefix, link, suffix = match.groups()
        if re.match(r"https?://", link):
            return match.group(0)
        if is_root:
            new_link = re.sub(r"^(?:\./)?(?:docs/)?", "", link)
            new_link = "./" + new_link
            return f"{prefix}{new_link}{suffix}"
        else:
            return match.group(0)

    content = img_pattern.sub(replace_img, content)

    return content


def process_file(file_path: str):
    """
    Load files and save translated content for each language.
    - For root README.md, save to docs/README_<lang>.md.
    - For other files, save to the same directory with _<lang> suffix.
    """
    logger.info("Processing file: %s", file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    is_root = os.path.dirname(file_path) == "" and re.search(
        r"readme", os.path.basename(file_path), re.IGNORECASE
    )
    for lang_code in LANGUAGES:
        logger.info("Translating %s to %s", file_path, lang_code)
        try:
            translated = translate_text(content, lang_code)
            # translated = content  # For debug (It can skip the time-consuming translation process)
        except Exception as e:
            logger.error("Translation failed for %s: %s", lang_code, e)
            continue

        if is_root:
            # For root README.md
            output_dir = "docs"
            base_name, ext = os.path.splitext(os.path.basename(file_path))
            output_file = os.path.join(output_dir, f"{base_name}_{lang_code}{ext}")
        else:
            # For other files on docs/
            output_dir = os.path.dirname(file_path)
            base_name, ext = os.path.splitext(os.path.basename(file_path))
            output_file = os.path.join(output_dir, f"{base_name}_{lang_code}{ext}")

        os.makedirs(output_dir, exist_ok=True)
        logger.info("Updating links for %s in language: %s", file_path, lang_code)
        translated = update_links(translated, lang_code, output_file, is_root=is_root)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated)
        logger.info("Saved translated file to %s", output_file)


def is_source_file(file_path: str) -> bool:
    """
    Return True if file_path is a source file (not already translated).
    """
    if file_path.lower().startswith("readme"):
        return True
    if not file_path.startswith("docs/"):
        return False
    base_name = os.path.basename(file_path)
    for lang in LANGUAGES:
        if base_name.endswith(f"_{lang}.md"):
            return False
    return True


def get_source_files() -> list[str]:
    """
    Get a list of source Markdown files to translate.
    Includes the root README.md and any files under docs/ that are not already translated.
    """
    source_files = []
    if os.path.exists("README.md"):
        source_files.append("README.md")
    for root, dirs, files in os.walk("docs"):
        # LANGUAGES で定義された言語ディレクトリは除外
        dirs[:] = [d for d in dirs if d not in LANGUAGES]
        for file in files:
            if file.lower().endswith(".md"):
                file_path = os.path.join(root, file).replace(os.sep, "/")
                if is_source_file(file_path):
                    source_files.append(file_path)
    return source_files


def main():
    logger.info("Starting translation process")
    check_env_vars()

    try:
        with open("process_all.txt", "r") as f:
            process_all = f.read().strip().lower() == "true"
    except FileNotFoundError:
        logger.info(
            "process_all.txt not found, defaulting to process_all = True for debugging"
        )
        process_all = True

    if process_all:
        logger.info("Processing all source files (workflow_dispatch mode)")
        source_files = get_source_files()
        logger.info("Source files to process: %s", source_files)
        for file_path in source_files:
            logger.info("Processing %s", file_path)
            process_file(file_path)
    else:
        logger.info("Processing only changed files (PR mode)")
        try:
            with open("changed_files.txt", "r") as f:
                changed_files = set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            logger.error("changed_files.txt not found")
            sys.exit(1)
        logger.info("Changed files: %s", changed_files)
        source_files = {f for f in changed_files if is_source_file(f)}
        logger.info("Source files to process: %s", source_files)
        for file_path in source_files:
            logger.info("Processing %s", file_path)
            process_file(file_path)

    logger.info("Translation process completed.")


if __name__ == "__main__":
    main()
