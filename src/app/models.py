from pydantic import BaseModel


class EngineRequest(BaseModel):
    """
	   This schema contains how a request should be.
	   It contains a string that contains an image path and a boolean that tells us if we want white or transparent background.
	   """
    img: str
    remove_white: bool

    class Config:
        schema_extra = {"example": {"img": "C/User/Alpha/Pictures/1.jpg", "remove_white": True}}


class EngineResponse(BaseModel):
    img_cropped: str
    message: str

    class Config:
        schema_extra = {"example": {"img": "C/User/Alpha/Pictures/1_cropped.jpg", "message": "You image has been processed succesfully."}}
