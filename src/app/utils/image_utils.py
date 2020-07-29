import base64
import uuid
import cv2
import numpy as np
import requests
from PIL import Image

from app import *


def download(image_url):
    """
    Downloads an image given an Internet accessible URL.
    :param image_url: Internet accessible URL.
    :return: Output path of the downloaded image.
    """
    output_path= None
    response = requests.get(image_url, timeout=15)
    if response.ok:
        output_path = f"{DATA_FOLDER}/{uuid.uuid4()}.png"
        with open(output_path, "wb") as f:
            f.write(response.content)
    return output_path


def decode(image_base64):
    """
    Decodes an encoded image in base64.
    :param image_base64: Encoded image.
    :return: numpy array representing the image
    """
    img = base64.urlsafe_b64decode(image_base64.encode(encoding='utf-8'))
    img= np.frombuffer(img, dtype=np.float64)
    img = cv2.imdecode(img, flags=1)
    return img


def encode(output_image_path):
    """
    Encodes an image in base64 given its path.
    :param output_image_path: Image path.
    :return: Encoded image.
    """
    with open(output_image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def is_white(r, g, b):
    """
    Check if an RGB code is white.
    :param r: Red byte.
    :param g: Green byte.
    :param b: Blue byte.
    :return: True if the pixel is white, False otherwise.
    """
    if r == 255 and g == 255 and b == 255:
        return True
    else:
        return False


def remove_white(image_path):
    """
    Remove the color white of an image given its path.
    :param image_path: Image path.
    :return: Image saved without white color.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGBA")

        new_data = []
        for item in img.getdata():
            if is_white(item[0], item[1], item[2]):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(image_path, format="PNG", quality=95)


def get_resize_dimensions(original_size, dimensions):
    """
    Gets the ideal resize dimensions given the original size.
    :param original_size: Original size.
    :param dimensions: Default target dimensions.
    :return: Ideal dimensions.
    """
    dim_x, dim_y = dimensions
    img_x, img_y = original_size
    if img_x >= img_y:
        return int(dim_x), int(img_y * (dim_x / (img_x * 1.0)))
    else:
        return int(img_x * (dim_y / (img_y * 1.0))), int(dim_y)
