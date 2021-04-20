import os
import cv2
import uuid
import numpy as np

from scipy import ndimage
from PIL import Image, ImageOps

from src import TMP_FOLDER


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """
    Return a sharpened version of the image, using an unsharp mask.
    :param image: Input image.
    :param kernel_size: Size of the kernel use for the morphology operation.
    :param sigma: Parameter used for the Gaussian Blur.
    :param amount: Parameter to control sharpening.
    :param threshold: Parameter to control sharpening.
    """
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def crop(image, mask_path, to_remove, color_removal):
    """"
    :param image: Input image.
    :param mask_path: The mask given by the model.
    :param to_remove: Element to remove the input image result.
    :param color_removal: Color from the removed or erased part.
    :return: The output image.
    """
    image_original = Image.fromarray(np.uint8(image))
    mask = np.array(Image.open(mask_path))
    # threshold mask
    idx = mask >= 5
    mask[idx] = 255
    idx = mask < 5
    mask[idx] = 0
    
    # Sharpening algorithm
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
    mask = ndimage.gaussian_filter(mask, sigma=(2, 2), order=0)
    mask = unsharp_mask(mask, amount=15.0)
    
    # Put alpha
    mask = cv2.resize(mask, dsize=image_original.size, interpolation=cv2.INTER_LANCZOS4)
    mask = Image.fromarray(mask).convert('L')
    if to_remove == 'foreground':
        mask = ImageOps.invert(mask)
    if color_removal == 'white':
        background = Image.new('RGB', mask.size, (255, 255, 255))
    else:
        background = Image.new('RGBA', mask.size, (255, 255, 255, 0))
    
    # Generate output image with the mask
    output_image = Image.composite(image_original, background, mask)
    output_image = output_image.resize(
        (image_original.width, image_original.height), resample=Image.LANCZOS
    )
    tmp_file_name = os.path.join(TMP_FOLDER, '{}.png'.format(uuid.uuid4()))
    output_image.save(tmp_file_name)
    return tmp_file_name
