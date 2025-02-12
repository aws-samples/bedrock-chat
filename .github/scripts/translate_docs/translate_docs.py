#!/usr/bin/env python3
import json
import logging
import os
import re
import sys

import boto3
from retry import retry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LANGUAGES = [
    "ja",
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


@retry(Exception, tries=5, delay=2, backoff=2)
def translate_text(text: str, target_lang: str) -> str:
    """
    Translation function using the AWS Bedrock Converse API.
    - For the first request, send the text to be translated as a user message.
    - If the response stopReason is "max_tokens", continue generating and concatenate the results.
    """
    logger.info("Starting translation for target language: %s", target_lang)
    region = os.environ.get("AWS_REGION")
    model = "haiku-3.5"
    model_id = get_model_id(model)
    logger.info("Using model_id: %s", model_id)

    system_prompt = {
        "text": (
            f"You are a translation assistant. Your task is to translate the following text into {target_lang}. "
            "Ignore any character limit and translate the entire text completely, regardless of length. "
            "Return only the translated text and nothing else. "
            "Keep all markdown formatting exactly as in the original text."
        )
    }

    user_message = {"role": "user", "content": [{"text": text}]}
    inference_config = {
        "maxTokens": 4096,
        "temperature": 0.7,
        "topP": 0.95,
    }
    payload = {
        "modelId": model_id,
        "inferenceConfig": inference_config,
        "system": [system_prompt],
        "messages": [user_message],
        "additionalModelRequestFields": {},
    }
    logger.debug("Payload for Converse API:\n%s", json.dumps(payload, indent=2))

    client = boto3.client("bedrock-runtime", region_name=region)
    logger.debug("Created boto3 client for bedrock-runtime in region %s", region)

    response = client.converse(**payload)
    logger.debug("Response from client.converse: %s", response)

    complete_text = ""
    if "output" in response and "message" in response["output"]:
        content_list = response["output"]["message"].get("content", [])
        if content_list and "text" in content_list[0]:
            complete_text = content_list[0]["text"]
    stop_reason = response.get("stopReason", "")

    while stop_reason == "max_tokens":
        logger.info("Token limit reached. Continuing translation...")
        continuation_payload = {
            "modelId": model_id,
            "inferenceConfig": inference_config,
            "system": [system_prompt],
            "messages": [
                user_message,
                {"role": "assistant", "content": [{"text": complete_text}]},
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "Please continue the translation from where you left off."
                        }
                    ],
                },
            ],
            "additionalModelRequestFields": {},
        }
        logger.debug(
            "Continuation payload:\n%s", json.dumps(continuation_payload, indent=2)
        )
        new_response = client.converse(**continuation_payload)
        logger.debug("Continuation response: %s", new_response)
        new_text = ""
        if "output" in new_response and "message" in new_response["output"]:
            content_list = new_response["output"]["message"].get("content", [])
            if content_list and "text" in content_list[0]:
                new_text = content_list[0]["text"]
        complete_text += new_text
        stop_reason = new_response.get("stopReason", "")
    if not complete_text:
        logger.error("No text found in the response")
        raise Exception("No text found in the response")
    logger.info("Translation successful for target language: %s", target_lang)
    return complete_text


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
            # If the link starts with "./docs/imgs/" or "docs/imgs/", convert it to "./imgs/…"
            if re.match(r"^(\./)?docs/imgs/", link_target):
                new_target = re.sub(r"^(\./)?docs/imgs/", "./imgs/", link_target)
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


def main():
    logger.info("Starting translation process")
    check_env_vars()

    # For root README.md
    if os.path.exists("README.md"):
        logger.info("Processing root README.md")
        process_file("README.md")

    # For all files under docs/
    for root, dirs, files in os.walk("docs"):
        dirs[:] = [d for d in dirs if d not in LANGUAGES]
        for file in files:
            if file.lower().endswith(".md"):
                file_path = os.path.join(root, file)
                process_file(file_path)
    logger.info("Translation process completed.")


if __name__ == "__main__":
    main()
