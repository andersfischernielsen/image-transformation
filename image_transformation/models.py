from pydantic import BaseModel


class Base64Image(BaseModel):
    base64: str


class CenterCropRequest(BaseModel):
    image: Base64Image
    width: int
    height: int


class CenterCropResponse(BaseModel):
    image: Base64Image


class DifferenceRequest(BaseModel):
    base: Base64Image
    diff: Base64Image
    threshold: float = 0.0


class DifferenceResponse(BaseModel):
    image: Base64Image
    distortion: float = 0.0


class ImageHashRequest(BaseModel):
    image: Base64Image


class ImageHashResponse(BaseModel):
    hash: str
