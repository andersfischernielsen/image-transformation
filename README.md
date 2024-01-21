# image-transformation
A small Python API for transforming images. 

## Running the project
The project assumes that either a container runtime (Docker, OrbStack, etc.) or a Python/[Poetry](https://python-poetry.org/docs/#installation) runtime is available on the system. If a Python/Poetry runtime is used, an installation of [ImageMagick](https://formulae.brew.sh/formula/imagemagick) is also expected to be present on the system.


### Running via `docker compose`
```sh
docker compose up
```

### Running via `docker`
```sh
docker build -t image-transformation .
docker run image-transformation -p 8080:8080
```

### Running via `poetry`
```sh 
poetry install
poetry run python image_transformation.app
```

### `cURL`ing the API
The API can be accessed on `localhost:8080` once running. An OpenAPI specification of the API is available at `/openapi.json` for import into e.g. [Insomnia](https://insomnia.rest/) or [Postman](https://www.postman.com/).

Examples of `cURL`ing the API can be seen below. 

<details>
<summary><code>form-data cURL</code></summary>
<pre>
curl --request POST \
  --url http://localhost:8080/v1/images/difference \
  --header 'Content-Type: multipart/form-data' \
  --header 'User-Agent: insomnia/8.4.5' \
  --form base=@/YOUR-PATH-HERE/image1.jpg \
  --form diff=@/YOUR-PATH-HERE/image2.png \
  --form threshold=0.2
</pre>
</details>

<details>
<summary><code>JSON/base64 cURL</code></summary>
<pre>
curl --request POST \
  --url http://localhost:8080/v2/images/center-crop \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/8.4.5' \
  --data '{
	"image": {
		"base64": "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"
	}, 
	"width": 422,
	"height": 42
}'
</pre>
</details>

## Implementation details

The project contains a simple Python FastAPI API for receiving images and performing three main operations on images: 
- cropping from the center of a given image
- comparison of two images ([pixel-by-pixel comparison of ImageMagick](https://www.imagemagick.org/Usage/compare/))
- SHA-256 hashing of images

The project relies on [ImageMagick](https://imagemagick.org/index.php) to accomplish these image processing tasks. ImageMagick was chosen for the project since it is a well-regarded and popular library in both the web and graphic design communities because of its power and flexibility when it comes to working on images, for scripting and automation of image processing in general through its API. The Python wrapper used for the project is [Wand](https://docs.wand-py.org/en/0.6.13/), since it allows accessing the functionality of ImageMagick in a more Pythonic way while being well-maintained and providing documentation covering the ImageMagick functionality it provides.
The provided functions can of course be extended to e.g. support different [metrics](https://imagemagick.org/script/command-line-options.php#metric) for image comparison, fuzzy pixel difference matching, [image](https://huggingface.co/tasks/image-segmentation) [segmentation](https://cdn.openai.com/papers/GPTV_System_Card.pdf) [analysis](https://llava-vl.github.io/) comparisons, or existing features could also be extended, so e.g. the image comparison would not expect similar dimensionality of images, etc.. These potential features have been omitted due to time and a wish to keep the project small, lean and easy to extend. 

The project contains two APIs, `v1` and `v2`. The APIs are identical in implementation, but supports different request types. `v1` supports classic form data uploading of images and options for processing, while `v2` supports a more modern JSON/base64-based approach to API design and request/response types.
Both APIs present identical response types to clients, allowing clients to consume the API in a simple manner while providing flexibility in how the API functionality is used from the client's perspective.

The project also relies on `poetry`, `ruff`, `pydantic` and `mypy` to provide a solid Python development environment. Configuration for automatic debugging of both local and containerized Python runtimes is also provided for VSCode. 

## Implementation Timeline

### 1 Hour
- Setting up a decent containerization setup with
    - a multi-stage container build
    - composition of the container to allow running the container in a reproducible way
    - allowing debugging of the application in a containerized environment

- Setting up a decent Python environment using
    - Poetry for free virtual environments and easy dependency conflict resolution
    - Ruff for fast formatting/linting
    - MyPy/Pydantic for strict type checking

### 2 hours

- Research various [ImageMagick](https://imagemagick.org/index.php) binding libraries for Python before settling on [Wand](https://docs.wand-py.org/en/0.6.13/)
- Creating an initial JSON-based API relying on base64 encoded images before realizing the documentation specifies binary data formats explicitly
- Invent a story where the initial version of the API used form-data encoding before releasing a new version of the API using JSON request bodies
- Add additional request handling for the `v1` and `v2` APIs, respectively

### 1 hour

- Add an initial `pytest` test harness and a number of postive and negative tests


---

_Break_

---

### 1 hour
- Project polishing (comments, readability, separation of concerns, tests) and writing this `README`.
