from fastapi import FastAPI
import uvicorn

from image_transformation import get_env
from image_transformation.api import health
from image_transformation.api.v1 import v1
from image_transformation.api.v2 import v2

app = FastAPI()

app = health(app)
app = v1(app)
app = v2(app)

host = get_env("HOST", "localhost")
port = int(get_env("PORT", "8080"))

uvicorn.run(app, host=host, port=port)
