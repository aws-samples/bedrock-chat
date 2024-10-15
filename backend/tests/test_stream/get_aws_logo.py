import base64
from io import BytesIO

import requests


def get_png_bytes_from_url(url: str) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()

        if "image/png" not in response.headers.get("Content-Type", ""):
            raise ValueError("Content-Type is not image/png")

        return BytesIO(response.content).getvalue()

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch image from {url}: {str(e)}")
    except ValueError as e:
        raise Exception(str(e))


def get_aws_logo() -> bytes:
    URL = "https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_179x109.png"
    return get_png_bytes_from_url(URL)


def get_cdk_logo() -> bytes:
    URL = "https://docs.aws.amazon.com/cdk/api/v2/img/cdk-logo-small.png"
    return get_png_bytes_from_url(URL)
