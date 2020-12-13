import os
import base64
import time
import requests

from PIL import Image, ImageFile
from src import TMP_FOLDER
from src.utils import log, storage


ImageFile.LOAD_TRUNCATED_IMAGES = True


def download(correlation_id, image_url, output_path=None):
    """
    Downloads an image given an Internet accessible URL.
    :param correlation_id: Unique identifier for specific request.
    :param image_url: Internet accessible URL.
    :param output_path: Output path where the image should go.
    :return: Output path of the downloaded image.
    """
    try:
        response = requests.get(image_url, timeout=15)
        if response.ok:
            if not output_path:
                output_path = os.path.join(TMP_FOLDER, '{}.png'.format(correlation_id))
            with open(output_path, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        log.warn('Error downloading [{}]: [{}]'.format(image_url, e))
        output_path = None
    return output_path


def upload(correlation_id, output_image_path):
    """
    Uploads an image given its path to an accessible URL.
    :param correlation_id: Unique identifier for specific request.
    :param output_image_path: Image path.
    :return: Accessible image URL
    """
    for attempt in range(3):
        try:
            return storage.upload_image(correlation_id, output_image_path)
        except Exception as e:
            time.sleep(attempt + 1)
            log.warn(f'Error uploading image [{output_image_path}] to Storage: [{e}]')
    return None


def decode(correlation_id, image_base64, output_path=None):
    """
    Decodes an encoded image in base64.
    :param correlation_id: Unique identifier for specific request.
    :param image_base64: Encoded image.
    :param output_path: Output path where the image should go.
    :return: Output path of the decoded image.
    """
    try:
        image_data = base64.b64decode(image_base64)
        if not output_path:
            output_path = os.path.join(TMP_FOLDER, '{}.png'.format(correlation_id))
        with open(output_path, 'wb') as f:
            f.write(image_data)
        with Image.open(output_path).convert('RGBA') as img:
            img.save(output_path, format='PNG', quality=95)
    except Exception as e:
        log.warn('Error decoding [{}...] to [{}]: [{}]'.format(image_base64[:10], output_path, e))
        output_path = None
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


def get_dimensions(image_path):
    """
    Get dimensions from an image given its path.
    :param image_path: Image path to retrieve dimensions.
    :return: Tuple with width and height.
    """
    with Image.open(image_path) as img:
        return img.size


def resize(image_path, target_dimensions, image_format):
    """
    Resize image given the target dimensions, saving it in the same file.
    :param image_path: Image path to resize.
    :param target_dimensions: Dimensions to resize image.
    :param image_format: Image saved format.
    :return: Image resized saved in the same as given.
    """
    with Image.open(image_path) as img:
        img = img.resize(target_dimensions, resample=Image.LANCZOS)
        if image_format == 'PNG':
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        img.save(image_path, format=image_format, quality=95)


def resize_aspect(image_path, original_dimensions, largest_size_target, image_format):
    """
    Resize image keeping aspect ratio, saving it in the same file.
    :param image_path: Image path to resize.
    :param original_dimensions: Dimensions from original image.
    :param largest_size_target: Largest size target to resize.
    :param image_format: Image saved format.
    :return: Image resized saved in the same as given.
    """
    img_x, img_y = original_dimensions
    if img_x >= img_y:  # e.g. 1024x768
        target_dims = max(int(largest_size_target), 1), max(int(img_y * (largest_size_target / (img_x * 1.0))), 1)
    else:  # e.g. 768x1024
        target_dims = max(int(img_x * (largest_size_target / (img_y * 1.0))), 1), max(int(largest_size_target), 1)
    resize(image_path, target_dims, image_format)
