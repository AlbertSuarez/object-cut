import os

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
model_path = os.path.join("models", "Model.u2net.name.pth")
log.info("Model path: [{}]".format(model_path))
net = define_model(Model[Model.u2net.name], model_path, gpu=True)
log.info("Model loaded")


@app.get("/")
def health_check():
    return {"code": 200, "message": "API is hella working!"}


@app.post("/predict", response_model=EngineResponse, tags=["predictions"])
def predict(request: EngineRequest):
    try:
        result = run(net, request.image, request.remove_white, gpu=True)
        log.info("Generating image")
        return {
            "image_cropped": result,
            "message": "Your image has been processed succesfully.",
        }

    except Exception as e:
        log.error(e)
        return {"image_cropped": "", "message": f"{e}"}
