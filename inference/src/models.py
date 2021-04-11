from pydantic import BaseModel

from src import EXAMPLE_IMAGE_PATH, EXAMPLE_MASK_PATH, EXAMPLE_MESSAGE_SUCCESS


class EngineRequest(BaseModel):
    """
    This schema contains how a request should be.
    It contains a string that contains an image path and a boolean that tells us if we want white or transparent bg.
    """

    img: str
    to_remove: str
    color_removal: str
    secret_access: str

    class Config:
        schema_extra = dict(example=dict(
            img=EXAMPLE_IMAGE_PATH, to_remove='background', color_removal='transparent', secret_access='SECRET'
        ))


class EngineResponse(BaseModel):
    """
    This schema contains how a response should be.
    It contains a boolean telling you if the requests was successful or not along with a message
    and an image path containing the result image.
    """

    error: bool
    mask: str
    message: str

    class Config:
        schema_extra = dict(example=dict(
            error=False, mask=EXAMPLE_MASK_PATH, message=EXAMPLE_MESSAGE_SUCCESS
        ))
