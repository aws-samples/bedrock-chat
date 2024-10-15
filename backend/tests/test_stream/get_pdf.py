import base64
import os

import requests


def get_pdf_info(url) -> tuple[str, bytes]:
    response = requests.get(url)

    if response.status_code == 200:
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        else:
            filename = os.path.basename(url)

        return filename, response.content
    else:
        raise Exception(f"Failed to fetch PDF from {url}")


def get_aws_overview() -> tuple[str, bytes]:
    # Get the AWS Activate General 4 PDF as base64 encoded string
    URL = "https://aws-startup.s3.ap-northeast-1.amazonaws.com/Activate/AWS_Activate_General_4.pdf"
    return get_pdf_info(URL)


def get_test_markdown() -> str:
    return "##\nThis is a test text."
