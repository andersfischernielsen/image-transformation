from fastapi import UploadFile
from wand.image import Image as WandImage
from wand.color import Color
from base64 import b64decode, b64encode
from image_transformation.models import Base64Image


def load_base64(image: Base64Image) -> WandImage:
    decoded = b64decode(image.base64)
    try:
        return WandImage(blob=decoded)
    except Exception:
        raise ValueError("Image blob is in an invalid format")


def load_file(image: UploadFile) -> WandImage:
    blob = image.file.read()
    try:
        return WandImage(blob=blob)
    except Exception:
        raise ValueError("Image blob is in an invalid format")


def base64_encode(image: WandImage) -> str:
    try:
        blob = image.make_blob()
        if not blob:
            raise ValueError("Image blob is empty")

        return b64encode(blob).decode("utf-8")
    except Exception:
        raise ValueError("Image blob is in an invalid format")


def center_crop(image: WandImage, width: int, height: int) -> Base64Image:
    image.crop(width=width, height=height, gravity="center")
    encoded = base64_encode(image)
    return Base64Image(base64=encoded)


def difference(
    base: WandImage, diff: WandImage, threshold: float
) -> tuple[Base64Image, float]:
    base.fuzz = threshold
    difference, distortion = base.compare(
        diff, highlight=Color("red"), lowlight=Color("green")
    )
    encoded = base64_encode(difference)
    return Base64Image(base64=encoded), distortion


def hash(image: WandImage) -> str:
    if image.signature:
        return str(image.signature)
    else:
        raise ValueError("Image signature is empty")
