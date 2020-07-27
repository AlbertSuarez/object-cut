import time
import warnings

import cv2
import numpy as np
import torch
from PIL import Image
from scipy import ndimage
from torch.autograd import Variable
from torchvision import transforms

from src.u2_net.data_loader import RescaleT, ToTensorLab
from src.utils import log
from src.utils.image_utils import decode


def _load_img(image):
    """
    Create DataLoader instance form input path list.
    :param image: image.
    :return: DataLoader instance.
    """
    label_3 = np.zeros(image.shape)

    label = np.zeros(label_3.shape[0:2])
    if 3 == len(label_3.shape):
        label = label_3[:, :, 0]
    elif 2 == len(label_3.shape):
        label = label_3

    if 3 == len(image.shape) and 2 == len(label.shape):
        label = label[:, :, np.newaxis]
    elif 2 == len(image.shape) and 2 == len(label.shape):
        image = image[:, :, np.newaxis]
        label = label[:, :, np.newaxis]

    sample = dict(image=image, label=label)
    transforms.Compose([RescaleT(320), ToTensorLab(flag=0)])
    sample = transforms(sample)

    return sample


def define_model(model, model_path, gpu):
    """
    Define model given some parameters.
    :param model: Model enumeration.
    :param model_path: Model file path.
    :param gpu: If GPU is available or not.
    :return: Model instance.
    """
    net = model.value()
    if gpu:
        net.load_state_dict(torch.load(model_path))
        if torch.cuda.is_available():
            net.cuda()
    else:
        net.load_state_dict(torch.load(model_path, map_location="cpu"))
    net.eval()
    return net


# noinspection PyUnresolvedReferences
def _normalize_prediction(prediction):
    """
    Normalize the predicted SOD probability map.
    :param prediction: Model prediction.
    :return: Prediction normalized.
    """
    maximum = torch.max(prediction)
    minimum = torch.min(prediction)
    prediction_normalized = (prediction - minimum) / (maximum - minimum)
    return prediction_normalized


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


def run(net, image, remove_white_bg):
    """
    Run inference using U^2-Net model.
    :param net: model loaded
    :param image: Input image
    :param remove_white_bg: Boolean that shows if we have to remove white background or not
    :return: The image processed.
    """
    warnings.simplefilter("ignore", UserWarning)
    image_original = decode(image)
    sample = _load_img(image_original)
    inputs_test = sample["image"].unsqueeze(0)
    inputs_test = inputs_test.type(torch.FloatTensor)
    # Inference
    try:
        start_time = time.time()
        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        # Inference
        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        # Normalize
        prediction = d1[:, 0, :, :]
        prediction = _normalize_prediction(prediction)

        prediction = prediction.squeeze()
        prediction = prediction.cpu().data.numpy()
        prediction = prediction * 255

        # threshold mask
        idx = prediction >= 5
        prediction[idx] = 255
        idx = prediction < 5
        prediction[idx] = 0

        # SHARPENING ALGORITHM
        prediction = cv2.erode(prediction, np.ones((5, 5), np.uint8), iterations=1)
        prediction = ndimage.gaussian_filter(prediction, sigma=(2, 2), order=0)
        prediction = unsharp_mask(prediction, amount=3.0)
        # put alpha
        mask = Image.fromarray(prediction).convert("L")
        if remove_white_bg:
            background = Image.new("RGB", mask.size, (255, 255, 255))
        else:
            background = Image.new("RGBA", mask.size, (255, 255, 255, 0))

        # Generate output image with the mask
        image_original = Image.fromarray(image_original * 255).convert("RGB")
        output_image = Image.composite(image_original, background, mask)
        output_image = output_image.resize(
            (image_original.width, image_original.height), resample=Image.LANCZOS
        )

        # Clean
        del d1, d2, d3, d4, d5, d6, d7

        total_time = (time.time() - start_time) * 1000.0
        log.info("{:.2f}ms".format(total_time))
        return output_image

    except Exception as e:
        log.error("Error [{}]".format(e))
