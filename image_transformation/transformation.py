from fastapi import UploadFile
from wand.image import Image as WandImage
from wand.color import Color
from base64 import b64decode, b64encode
from image_transformation.models import (
    Base64Image,
    CenterCropRequest,
    CenterCropResponse,
    DifferenceRequest,
    DifferenceResponse,
    ImageHashRequest,
    ImageHashResponse,
)


# Helpers
def __load_base64(image: Base64Image) -> WandImage:
    decoded = b64decode(image.base64)
    try:
        return WandImage(blob=decoded)
    except Exception:
        raise ValueError("Image blob is in an invalid format")


def __load_file(image: UploadFile) -> WandImage:
    blob = image.file.read()
    try:
        return WandImage(blob=blob)
    except Exception:
        raise ValueError("Image blob is in an invalid format")


def __base64_encode(image: WandImage) -> str:
    blob = image.make_blob()
    if not blob:
        raise ValueError("Image blob is empty")

    return b64encode(blob).decode("utf-8")


# Transformations
def center_crop(image: WandImage, width: int, height: int) -> Base64Image:
    image.crop(width=width, height=height, gravity="center")
    encoded = __base64_encode(image)
    return Base64Image(base64=encoded)


def difference(
    base: WandImage, diff: WandImage, threshold: float
) -> tuple[Base64Image, float]:
    base.fuzz = threshold
    difference, distortion = base.compare(
        diff, highlight=Color("red"), lowlight=Color("green")
    )
    encoded = __base64_encode(difference)
    return Base64Image(base64=encoded), distortion


def hash(image: WandImage) -> str:
    if image.signature:
        return str(image.signature)
    else:
        raise ValueError("Image signature is empty")


# Form-data request handlers
def form_data_center_crop(
    request: UploadFile, height: int, width: int
) -> CenterCropResponse:
    image = __load_file(request)
    cropped = center_crop(image=image, height=height, width=width)
    return CenterCropResponse(image=cropped)


def form_data_difference(
    base: UploadFile, diff: UploadFile, threshold: float
) -> DifferenceResponse:
    loaded_base = __load_file(base)
    loaded_diff = __load_file(diff)

    image, distortion = difference(
        base=loaded_base, diff=loaded_diff, threshold=threshold
    )
    return DifferenceResponse(image=image, distortion=distortion)


def form_data_hash(request: UploadFile) -> ImageHashResponse:
    image = __load_file(request)
    return ImageHashResponse(hash=hash(image))


# JSON/base64 request handlers
def base64_center_crop(request: CenterCropRequest) -> CenterCropResponse:
    image = __load_base64(request.image)
    cropped = center_crop(image=image, height=request.height, width=request.width)
    return CenterCropResponse(image=cropped)


def base64_difference(request: DifferenceRequest) -> DifferenceResponse:
    base = __load_base64(request.base)
    diff = __load_base64(request.diff)

    image, distortion = difference(base=base, diff=diff, threshold=request.threshold)
    return DifferenceResponse(image=image, distortion=distortion)


def base64_hash(request: ImageHashRequest) -> ImageHashResponse:
    image = __load_base64(request.image)
    return ImageHashResponse(hash=hash(image))
