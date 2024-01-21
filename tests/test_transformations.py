import os
import sys
import pytest
from wand.image import Image as WandImage
from image_transformation.transformation import center_crop, difference, hash

images = os.path.join(os.getcwd(), "images")
image_files = os.listdir(images)
image_files = list(
    filter(
        lambda x: x.endswith(".jpg") or x.endswith(".png") or x.endswith(".jpeg"),
        image_files,
    )
)


def test_center_crops_all_known_good_images():
    for filename in image_files:
        filename, file_extension = os.path.splitext(filename)
        with WandImage(
            filename=os.path.join(images, filename + file_extension),
            format=file_extension.replace(".", ""),
        ) as img:
            center_crop(img, 100, 100)


def test_throws_on_negative_cropping_dimensions():
    with pytest.raises(ValueError):
        with WandImage(filename=os.path.join(images, "image0.jpeg")) as img:
            center_crop(img, -100, -100)


def test_supports_empty_cropping_dimensions():
    with pytest.raises(ValueError):
        with WandImage(filename=os.path.join(images, "image0.jpeg")) as img:
            center_crop(img, 0, 0)


def test_supports_large_cropping_dimensions():
    with WandImage(filename=os.path.join(images, "image0.jpeg")) as img:
        center_crop(img, sys.maxsize, sys.maxsize)


def test_supports_large_thresholds():
    with WandImage(filename=os.path.join(images, "image0.jpeg")) as base:
        with WandImage(filename=os.path.join(images, "image0.jpeg")) as diff:
            difference(base, diff, float(sys.maxsize))


def test_does_not_support_negative_thresholds():
    with WandImage(filename=os.path.join(images, "image0.jpeg")) as base:
        with WandImage(filename=os.path.join(images, "image0.jpeg")) as diff:
            difference(base, diff, -2)


def test_finds_difference_all_known_good_images():
    for base, diff in zip(image_files[:-1], image_files[1:]):
        with WandImage(filename=os.path.join(images, base)) as base:
            with WandImage(filename=os.path.join(images, diff)) as diff:
                difference(base, diff, 0.5)


def test_hashes_all_known_good_images():
    for filename in image_files:
        with WandImage(filename=os.path.join(images, filename)) as img:
            hash(img)
