#!/usr/bin/env python3
import json
import logging
import os
import re
import sys

import boto3
from botocore.config import Config
from retry import retry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# LANGUAGES = [
#     "ja",
# ]

# Target languages for translation
LANGUAGES = [
    "de",
    "es",
    "fr",
    "it",
    "ja",
    "ko",
    "ms",
    "nb",
    "th",
    "vi",
    "zh-hans",
    "zh-hant",
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
    region = os.environ.get("AWS_REGION")
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
    # ## で始まる行で分割
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

    # 翻訳結果を結合（セクション間に空行を入れる）
    final_translation = "\n\n".join(complete_translation)

    logger.info("Translation completed for target language: %s", target_lang)
    return final_translation


def update_links(content: str, lang_code: str, rel_path: str) -> str:
    """
    Update links in the given content for the specified language and relative path.

    [Case 1] Root README.md (rel_path is "README.md"):
    - Markdown links: Replace links that start with "./docs/…" or "docs/…" with "./…"
    - Image links: Replace links that start with "./docs/imgs/…" or "docs/imgs/…" with "./imgs/…"


    [Case 2] All other cases (e.g., "subdir/file.md"):
    - No change for Markdown links
    - For image links: If the link starts with "imgs/" or "./imgs/", convert it to a relative path to "docs/imgs/"
        based on the depth of the output file (number of directory levels in rel_path).
        Example: If the output is "docs/ja/subdir/file.md" (depth 1), the prefix is "../"*(1+1) = "../../", so "../../imgs/…"

    【ケース1】 ルート README.md (rel_path が "README.md" の場合)
      - Markdown リンク: リンク先が "./docs/…" または "docs/…" を "./…" に変換
      - 画像リンク: リンク先が "./docs/imgs/…" または "docs/imgs/…" を "./imgs/…" に変換

    【ケース2】 それ以外 (例: "subdir/file.md")
      - Markdown リンクは変更なし
      - 画像リンク: リンク先が "imgs/…" または "./imgs/…" の場合、出力ファイルの深度 (rel_path のディレクトリ階層数) に合わせて、
        リポジトリ内の docs/imgs/ への相対パスに変換する。
        例: 出力先が "docs/ja/subdir/file.md" (深度 1) の場合、プレフィックスは "../"*(1+1) = "../../", で "../../imgs/…"
    """
    logger.debug("Updating links for lang_code: %s, rel_path: %s", lang_code, rel_path)
    depth = 0
    # ルートの場合は、file_path はルートにあるとみなすので、rel_path が "README.md"
    if os.path.dirname(rel_path):
        depth = len(os.path.dirname(rel_path).split(os.sep))

    # Case 1: Root README.md
    if depth == 0 and os.path.basename(rel_path).lower() == "readme.md":

        def replace_root_md(match: re.Match) -> str:
            link_text = match.group(1)
            link_target = match.group(2)
            # If the link starts with "./docs/" or "docs/", convert it to "./…"
            if re.match(r"^(\./)?docs/", link_target):
                new_target = re.sub(r"^(\./)?docs/", "./", link_target)
                logger.debug(
                    "Root README: Replacing md link: %s -> %s", link_target, new_target
                )
                return f"[{link_text}]({new_target})"
            return match.group(0)

        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_root_md, content)

        def replace_root_img(match: re.Match) -> str:
            alt_text = match.group(1)
            link_target = match.group(2)
            # If the link starts with "./docs/imgs/" or "docs/imgs/", convert it to "../imgs/…"
            if re.match(r"^(\./)?docs/imgs/", link_target):
                new_target = re.sub(r"^(\./)?docs/imgs/", "../imgs/", link_target)
                logger.debug(
                    "Root README: Replacing image link: %s -> %s", link_target, new_target
                )
                return f"![{alt_text}]({new_target})"
            return match.group(0)

        content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_root_img, content)
    else:
        # Case 2: Non-root files
        # Markdown links are left as is
        # For image links: If the link starts with "imgs/" or "./imgs/", convert it to a relative path to "docs/imgs/"
        prefix = "../" * (depth + 1)  # Note that output location is "docs/<lang_code>/"

        def replace_nonroot_img(match: re.Match) -> str:
            alt_text = match.group(1)
            link_target = match.group(2)
            if re.match(r"^(\./)?imgs/", link_target):
                new_target = prefix + "imgs/" + re.sub(r"^(\./)?imgs/", "", link_target)
                logger.debug(
                    "Non-root: Replacing image link: %s -> %s", link_target, new_target
                )
                return f"![{alt_text}]({new_target})"
            return match.group(0)

        content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_nonroot_img, content)
    return content


def process_file(file_path: str):
    logger.info("Processing file: %s", file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Set relative path based on whether the file is under docs/ or not
    if os.path.dirname(file_path) == "":
        # The case of root README.md
        rel_path = os.path.basename(file_path)
    else:
        # The case of files under docs/
        rel_path = os.path.relpath(file_path, "docs")
    logger.info("Relative path for file: %s", rel_path)
    is_root_readme = os.path.basename(
        rel_path
    ).lower() == "readme.md" and not os.path.dirname(rel_path)

    for lang_code in LANGUAGES:
        logger.info("Translating %s to %s", file_path, lang_code)
        try:
            translated = translate_text(content, lang_code)
            # translated = "test"
        except Exception as e:
            logger.error("Translation failed for %s: %s", lang_code, e)
            continue

        logger.info("Updating links for %s in language: %s", file_path, lang_code)
        translated = update_links(translated, lang_code, rel_path)

        # Create output directory if it doesn't exist
        if os.path.dirname(file_path) == "":
            output_dir = os.path.join("docs", lang_code)
        else:
            output_dir = os.path.join("docs", lang_code, os.path.dirname(rel_path))
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated)
        logger.info("Saved translated file to %s", output_file)


def get_source_files() -> list[str]:
    """
    Get all source markdown files that should be translated.
    Returns a list of file paths that are either:
    1. README.md in the root
    2. Markdown files under docs/ but not in language-specific directories
    """
    source_files = []

    # Add root README.md if it exists
    if os.path.exists("README.md"):
        source_files.append("README.md")

    # Add files under docs/
    for root, dirs, files in os.walk("docs"):
        # Exclude language-specific directories
        dirs[:] = [d for d in dirs if d not in LANGUAGES]

        for file in files:
            if file.lower().endswith(".md"):
                file_path = os.path.join(root, file)
                # Convert to use forward slashes for consistency
                file_path = file_path.replace(os.sep, "/")
                if is_source_file(file_path):
                    source_files.append(file_path)

    return source_files


def is_source_file(file_path: str) -> bool:
    """
    Check if the file is a source file (not in language-specific directories).
    Returns True if the file is either:
    1. README.md in the root
    2. A markdown file under docs/ but not in a language-specific directory
    """
    if file_path == "README.md":
        return True

    # Check if the file is under docs/
    if not file_path.startswith("docs/"):
        return False

    # Split the path into components
    parts = file_path.split("/")

    # If it's directly under docs/ (e.g., docs/README.md)
    if len(parts) == 2:
        return True

    # Check if the first directory under docs/ is a language code
    return parts[1] not in LANGUAGES


def main():
    logger.info("Starting translation process")
    check_env_vars()

    try:
        with open("process_all.txt", "r") as f:
            process_all = f.read().strip().lower() == "true"
    except FileNotFoundError:
        logger.error("process_all.txt not found")
        sys.exit(1)

    if process_all:
        # Workflow dispatch mode: process all source files
        logger.info("Processing all source files (workflow_dispatch mode)")
        source_files = get_source_files()
        logger.info("Source files to process: %s", source_files)

        for file_path in source_files:
            logger.info("Processing %s", file_path)
            process_file(file_path)
    else:
        # PR mode: process only changed source files
        logger.info("Processing only changed files (PR mode)")
        try:
            with open("changed_files.txt", "r") as f:
                changed_files = set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            logger.error("changed_files.txt not found")
            sys.exit(1)

        logger.info("Changed files: %s", changed_files)

        # Filter and process only source files
        source_files = {f for f in changed_files if is_source_file(f)}
        logger.info("Source files to process: %s", source_files)

        for file_path in source_files:
            logger.info("Processing %s", file_path)
            process_file(file_path)

    logger.info("Translation process completed.")


if __name__ == "__main__":
    main()
