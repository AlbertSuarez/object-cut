import os
import uuid
import numpy as np

from PIL import Image
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.models import EngineRequest, EngineResponse
from app.u2_net.run import define_model, run
from app.u2_net.model_enum import Model
from app.utils import log


app = FastAPI()


origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model_path = os.path.join("app", "data", "u2net.pth")
log.info("Model path: [{}]".format(model_path))
net = define_model(Model[Model.u2net.name], model_path, gpu=False)
log.info("Model loaded")


@app.get("/")
def health_check():
    return {"code": 200, "message": "API is hella working!"}


@app.post("/predict", response_model=EngineResponse, tags=["predictions"])
def predict(request: EngineRequest):
    log.info('Starting request')
    try:
        image = np.array(Image.open(request.img).convert('RGB'))
        result = run(net, image, request.remove_white)
        tmp_file_name = os.path.join('results', "{}.png".format(uuid.uuid4()))
        result.save(tmp_file_name)


        log.info("Image cropped saved in:{}".format(tmp_file_name))
        return {
            "img_cropped": tmp_file_name,
            "message": "Your image has been processed succesfully.",
        }

    except Exception as e:
        log.error(e)
        return {"image_cropped": 'None', "message": f"{e}"}
