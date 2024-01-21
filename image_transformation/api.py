from fastapi import FastAPI
from image_transformation import get_env
import uvicorn

app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


uvicorn.run(app, host=get_env("HOST", "localhost"), port=int(get_env("PORT", 8080)))
