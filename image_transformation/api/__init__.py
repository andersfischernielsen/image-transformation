from fastapi import FastAPI


def health(app: FastAPI) -> FastAPI:
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
