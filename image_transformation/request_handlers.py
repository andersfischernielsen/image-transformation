from fastapi import UploadFile
from image_transformation.models import (
    CenterCropRequest,
    CenterCropResponse,
    DifferenceRequest,
    DifferenceResponse,
    ImageHashRequest,
    ImageHashResponse,
)
from image_transformation.transformation import (
    load_base64,
    load_file,
    center_crop,
    difference,
    hash,
)


# Form-data request handlers
def form_data_center_crop(
    request: UploadFile, height: int, width: int
) -> CenterCropResponse:
    image = load_file(request)
    cropped = center_crop(image=image, height=height, width=width)
    return CenterCropResponse(image=cropped)


def form_data_difference(
    base: UploadFile, diff: UploadFile, threshold: float
) -> DifferenceResponse:
    loaded_base = load_file(base)
    loaded_diff = load_file(diff)

    image, distortion = difference(
        base=loaded_base, diff=loaded_diff, threshold=threshold
    )
    return DifferenceResponse(image=image, distortion=distortion)


def form_data_hash(request: UploadFile) -> ImageHashResponse:
    image = load_file(request)
    return ImageHashResponse(hash=hash(image))


# JSON/base64 request handlers
def base64_center_crop(request: CenterCropRequest) -> CenterCropResponse:
    image = load_base64(request.image)
    cropped = center_crop(image=image, height=request.height, width=request.width)
    return CenterCropResponse(image=cropped)


def base64_difference(request: DifferenceRequest) -> DifferenceResponse:
    base = load_base64(request.base)
    diff = load_base64(request.diff)

    image, distortion = difference(base=base, diff=diff, threshold=request.threshold)
    return DifferenceResponse(image=image, distortion=distortion)


def base64_hash(request: ImageHashRequest) -> ImageHashResponse:
    image = load_base64(request.image)
    return ImageHashResponse(hash=hash(image))
