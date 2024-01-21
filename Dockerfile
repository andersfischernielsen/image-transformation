# --- BUILD IMAGE ---

FROM python:3.11-slim as build_image

ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==1.7.1

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-root --no-ansi --no-interaction;

ARG IS_DEBUG=0
RUN if [ "$IS_DEBUG" = "1" ]; then poetry add debugpy; fi

RUN rm -rf $POETRY_CACHE_DIR

# --- RELEASE IMAGE ---

FROM python:3.11-slim as release_image

ENV FASTAPI_ENV=production

ENV HOST="0.0.0.0"
ENV PORT=8080
ENV VIRTUAL_ENV=/.venv
ENV PATH="/.venv/bin:$PATH"

COPY --from=build_image $VIRTUAL_ENV $VIRTUAL_ENV

COPY image_transformation ./image_transformation

RUN apt-get update && apt-get install -y \
  imagemagick \
  && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["python", "-m", "image_transformation.app"]
