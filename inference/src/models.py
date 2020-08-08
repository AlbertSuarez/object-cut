from pydantic import BaseModel

from src import EXAMPLE_IMAGE_PATH, EXAMPLE_MESSAGE_SUCCESS


class EngineRequest(BaseModel):
    """
    This schema contains how a request should be.
    It contains a string that contains an image path and a boolean that tells us if we want white or transparent bg.
    """

    img: str
    remove_white: bool

    class Config:
        schema_extra = dict(example=dict(
            img=EXAMPLE_IMAGE_PATH, remove_white=True
        ))


class EngineResponse(BaseModel):
    """
    This schema contains how a response should be.
    It contains a boolean telling you if the requests was successful or not along with a message
    and an image path containing the result image.
    """

    error: bool
    img: str
    message: str

    class Config:
        schema_extra = dict(example=dict(
            error=False, img=EXAMPLE_IMAGE_PATH, message=EXAMPLE_MESSAGE_SUCCESS
        ))