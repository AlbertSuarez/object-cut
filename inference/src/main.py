import os
import uuid
import numpy as np

from PIL import Image
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import EXAMPLE_MESSAGE_SUCCESS, TMP_FOLDER
from src.models import EngineRequest, EngineResponse
from src.u2_net.run import define_model, run
from src.u2_net.model_enum import Model
from src.utils import log


# Init FastAPI application
app = FastAPI()
origins = ['http://localhost']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Load model
model_path = os.path.join('data', 'u2net.pth')
log.info('Model path: [{}]'.format(model_path))
net = define_model(Model[Model.u2net.name], model_path, gpu=False)
log.info('Model loaded')


@app.get('/stillalive')
def health_check():
    return 'API is hella working!'


@app.post('/predict', response_model=EngineResponse, tags=['predictions'])
def predict(request: EngineRequest):
    log.info('Starting request...')
    try:
        # Open image
        image = np.array(Image.open(request.img).convert('RGB'))
        # Run inference
        result, error_message = run(net, image, request.remove_white)

        if result:
            # Save image
            tmp_file_name = os.path.join(TMP_FOLDER, '{}.png'.format(uuid.uuid4()))
            result.save(tmp_file_name)

            # Return
            log.info('Image saved in: {}'.format(tmp_file_name))
            return dict(error=False, img=tmp_file_name, message=EXAMPLE_MESSAGE_SUCCESS)
        else:
            return dict(error=True, img=None, message=error_message)

    except Exception as e:
        error_message = 'Error on request: [{}]'.format(e)
        log.error(error_message)
        log.exception(e)
        return dict(error=True, img=None, message=error_message)