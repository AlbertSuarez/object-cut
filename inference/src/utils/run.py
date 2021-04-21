import time
import warnings
import numpy as np
import torch

from PIL import Image
from torch.autograd import Variable
from torchvision import transforms

from src.utils.data_loader import RescaleT, ToTensorLab
from src.utils import log


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
    transform = transforms.Compose([RescaleT(320), ToTensorLab(flag=0)])
    sample = transform(sample)
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
        net.load_state_dict(torch.load(model_path, map_location='cpu'))
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


# noinspection PyArgumentList
@torch.no_grad()
async def run(net, image):
    """
    Run inference using U^2-Net model.
    :param net: model loaded.
    :param image: Input image.
    :return: The output mask.
    """
    warnings.simplefilter('ignore', UserWarning)
    sample = _load_img(image)
    inputs_test = sample['image'].unsqueeze(0)
    inputs_test = inputs_test.type(torch.FloatTensor)

    # Inference
    log.info('Starting inference')
    try:
        start_time = time.time()
        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)
        # Inference
        d1 = net(inputs_test)[0]
        # Normalize
        prediction = d1[:, 0, :, :]
        prediction = _normalize_prediction(prediction)

        prediction = prediction.squeeze()
        prediction = prediction.cpu().data.numpy()
        prediction = prediction * 255
        prediction = Image.fromarray(prediction).convert('L')

        # Clean
        del d1

        total_time = (time.time() - start_time) * 1000.0
        log.info('{:.2f}ms'.format(total_time))


        return prediction, None

    except Exception as e:
        error_message = 'Error on request: [{}]'.format(e)
        log.error(error_message)
        log.exception(e)
        return None, error_message
