import os
from io import BytesIO
import pytest
from wand.image import Image as WandImage
from fastapi import UploadFile
from base64 import b64encode, b64decode
from image_transformation.models import Base64Image

from image_transformation.transformation import base64_encode, load_base64, load_file

images = os.path.join(os.getcwd(), "images")
test_image = os.path.join(images, "image0.jpeg")


def test_loads_valid_base64():
    with WandImage(filename=test_image) as img:
        blob = img.make_blob()
        base64_image = b64encode(blob).decode("utf-8")  # type: ignore

    loaded_image = load_base64(Base64Image(base64=base64_image))

    assert isinstance(loaded_image, WandImage)
    assert loaded_image.size != 0


def test_loads_valid_files():
    with WandImage(filename=test_image) as img:
        blob = img.make_blob()
        upload_file = UploadFile(file=BytesIO(blob))  # type: ignore

    loaded_image = load_file(upload_file)

    assert isinstance(loaded_image, WandImage)
    assert loaded_image.size != 0


def test_base64_encodes_valid_file():
    with WandImage(filename=test_image) as img:
        base64_image = base64_encode(img)

    decoded = b64decode(base64_image)
    with WandImage(blob=decoded) as img:
        assert img.size != 0


def test_raises_on_empty_base64_values():
    with pytest.raises(ValueError):
        load_base64(Base64Image(base64=""))


def test_raises_when_loading_empty_files():
    upload_file = UploadFile(file=BytesIO(b""))  # type: ignore
    with pytest.raises(ValueError):
        load_file(upload_file)


def test_raises_on_empty_image_encodes():
    with WandImage() as img:
        with pytest.raises(ValueError):
            base64_encode(img)
