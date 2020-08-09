import os
import uuid
import base64
import requests

from PIL import Image
from src import TMP_FOLDER
from src.utils import log


def download(correlation_id, image_url, output_path=None):
    """
    Downloads an image given an Internet accessible URL.
    :param correlation_id: Unique identifier for specific request.
    :param image_url: Internet accessible URL.
    :param output_path: Output path where the image should go.
    :return: Output path of the downloaded image.
    """
    response = requests.get(image_url, timeout=15)
    if response.ok:
        if not output_path:
            output_path = os.path.join(TMP_FOLDER, '{}.png'.format(correlation_id))
        with open(output_path, 'wb') as f:
            f.write(response.content)
    return output_path


def upload(correlation_id, output_image_path):
    """
    Uploads an image given its path to an accessible URL.
    :param correlation_id: Unique identifier for specific request.
    :param output_image_path: Image path.
    :return: Accessible image URL
    """
    return 'https://example.com/{}.png'.format(correlation_id)


def decode(correlation_id, image_base64, output_path=None):
    """
    Decodes an encoded image in base64.
    :param correlation_id: Unique identifier for specific request.
    :param image_base64: Encoded image.
    :param output_path: Output path where the image should go.
    :return: Output path of the decoded image.
    """
    image_data = base64.b64decode(image_base64)
    if not output_path:
        output_path = os.path.join(TMP_FOLDER, '{}.png'.format(correlation_id))
    with open(output_path, 'wb') as f:
        f.write(image_data)
    with Image.open(output_path).convert('RGBA') as img:
        img.save(output_path, format='PNG', quality=95)
    return output_path


def encode(output_image_path):
    """
    Encodes an image in base64 given its path.
    :param output_image_path: Image path.
    :return: Encoded image.
    """
    with open(output_image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


def verify(image_path):
    """
    Verifies if a path pointing to an actual image.
    :param image_path: Image path to check.
    :return: True if it's an image, False otherwise.
    """
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        log.warn('Path [{}] does not point to an image: [{}]'.format(image_path, e))
        return False
