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
    URL = "https://awsj-tc.s3-ap-northeast-1.amazonaws.com/Operations/Manuals/Public_Private/PC/AWS%E3%83%88%E3%83%AC%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0%E5%8F%97%E8%AC%9B%E8%A6%81%E4%BB%B6+-+%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3+%E3%82%AF%E3%83%A9%E3%82%B9%E3%83%AB%E3%83%BC%E3%83%A0_Webex.pdf"
    return get_pdf_info(URL)


def get_test_markdown() -> str:
    return "##\nThis is a test text."
