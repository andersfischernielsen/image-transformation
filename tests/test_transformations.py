import os
from wand.image import Image as WandImage
from image_transformation.transformation import center_crop, difference, hash

images = os.path.join(os.getcwd(), "images")
image_files = os.listdir(images)
image_files = filter(
    lambda x: x.endswith(".jpg") or x.endswith(".png") or x.endswith(".jpeg"),
    image_files,
)


def test_center_crops_all_known_good_images():
    for filename in image_files:
        filename, file_extension = os.path.splitext(filename)
        with WandImage(
            filename=os.path.join(images, filename + file_extension),
            format=file_extension.replace(".", ""),
        ) as img:
            center_crop(img, 100, 100)


def test_finds_difference_all_known_good_images():
    for filename in image_files:
        with WandImage(filename=os.path.join(images, filename)) as img:
            difference(img, img, 0.0)


def test_hashes_all_known_good_images():
    for filename in image_files:
        with WandImage(filename=os.path.join(images, filename)) as img:
            hash(img)
