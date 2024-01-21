from fastapi import FastAPI, Response

from image_transformation.models import (
    CenterCropRequest,
    DifferenceRequest,
    ImageHashRequest,
)
from image_transformation.request_handlers import (
    base64_center_crop,
    base64_difference,
    base64_hash,
)


def v2(app: FastAPI) -> FastAPI:
    # The V2 API supports base64 encoded images
    @app.post("/v2/images/center-crop")
    def center_crop(request: CenterCropRequest):
        try:
            return base64_center_crop(request)
        except ValueError as e:
            return Response(content=str(e), status_code=422)

    @app.post("/v2/images/difference")
    def difference(request: DifferenceRequest):
        try:
            return base64_difference(request)
        except ValueError as e:
            return Response(content=str(e), status_code=422)

    @app.post("/v2/images/hash")
    def hash(request: ImageHashRequest):
        try:
            return base64_hash(request)
        except ValueError as e:
            return Response(content=str(e), status_code=422)

    return app
