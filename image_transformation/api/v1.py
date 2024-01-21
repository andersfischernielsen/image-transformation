from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile, Response
from image_transformation.transformation import (
    form_data_center_crop,
    form_data_difference,
    form_data_hash,
)


def v1(app: FastAPI) -> FastAPI:
    # The V1 API supports form-data uploads
    @app.post("/v1/images/center-crop")
    def center_crop(
        file: Annotated[UploadFile, File()],
        height: Annotated[int, Form()],
        width: Annotated[int, Form()],
    ):
        try:
            form_data_center_crop(file, height, width)
        except ValueError as e:
            return Response(content=str(e), status_code=422)

    @app.post("/v1/images/difference")
    def difference(
        base: Annotated[UploadFile, File()],
        diff: Annotated[UploadFile, File()],
        threshold: Annotated[float, Form()],
    ):
        try:
            return form_data_difference(base, diff, threshold)
        except ValueError as e:
            return Response(content=str(e), status_code=422)

    @app.post("/v1/images/hash")
    def hash(request: Annotated[UploadFile, File()]):
        try:
            return form_data_hash(request)
        except ValueError as e:
            return Response(content=str(e), status_code=422)

    return app
