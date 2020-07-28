import os
import base64

from io import BytesIO
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.models import EngineRequest, EngineResponse
from app.u2_net.run import define_model, run
from app.u2_net.model_enum import Model
from app.utils.image_utils import decode
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
        image_decoded = decode(request.img)
        result = run(net, image_decoded, request.remove_white)

        buffered = BytesIO()
        result.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())

        log.info("Generating image")
        return {
            "img_cropped": img_str,
            "message": "Your image has been processed succesfully.",
        }

    except Exception as e:
        log.error(e)
        return {"image_cropped": 'None', "message": f"{e}"}
