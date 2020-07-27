from pydantic import BaseModel


class EngineRequest(BaseModel):
    img: str
    remove_white: bool


class EngineResponse(BaseModel):
    image_cropped: str
    message: str
