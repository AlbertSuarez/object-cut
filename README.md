# Engine

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

⚙️ Core API of ObjectCut

This repository contains all the logic necessary to run the ObjectCut Engine. It also contains a simple API to run the model. 

## Requirements

1. Python 3.7+
2. Docker CE
3. Docker-compose

## Recommendations

Usage of [virtualenv](https://realpython.com/blog/python/python-virtual-environments-a-primer/) is recommended for package library / runtime isolation.

## Usage

To run the server, please execute the following from the root directory:

1. Pull models from [Git LFS](https://git-lfs.github.com/)

    ```bash
    git lfs fetch --all
    ```

2. Deploy the whole stuck (multiplexer, inference and traefik) with just this command.

    ```bash
    docker-compose up -d --build --scale multiplexer=1 --scale inference=1
    ```

_That's it_! You have ObjectCut running on port 80 routing traffic using _traefik_.


## Hitting the API

For running inference on an image just hit the `/remove` endpoint.

```bash
curl --location --request POST 'localhost:80/remove' \
        --header 'Content-Type: application/json' \
        --header 'Host: multiplexer' \
        --header 'X-Secret-Access: SECRET' \
        --data-raw '{"image_url": IMAGE_URL}'
```

Getting a response like this one:

```json
{
    "correlation_id": "02011199-9769-4999-b2c7-8d32cb17fc49",
    "error": false,
    "response": {
        "image_url": "https://example.com/image-result.png"
    }
}
```

## Run tests

1. Run ObjectCut locally

2. Move to multiplexer module

    ```bash
    cd multiplexer
    ```

3. Run tests

    ```bash
    python3 -m unittest discover -v
    ```

## Development

### Integrations

This API integrates with several external APIs which are listed below.

#### Google Cloud Storage

For being able to upload the image response to a public bucket for let the users download the output, we are using GCS for doing it once the users specify that in the `output_format=url` (default value) in the API request.

The integration is pretty simple. Every request is being authenticated using the service account JSON file under the `keys` folder where every output image is being upload to the `object-cut-images` bucket under a Life Cycle policy of *3 days* (this has been configured on the Google Cloud Console UI). Once the file has been uploaded (and make it public) the library itself it returns you the public URL that you can return to the user.

### How to add a new test

Create a new python file on the `multiplexer` module called `test_*.py` in `test.api.*` with the following structure:

```python
from test.base import BaseTestClass


class NewTest(BaseTestClass):

    def test_v0(self):
        expected = 5
        result = 2 + 3
        self.assertEqual(expected, result)

```

### To Do

- [x] Deleted data Loader from original U2Net: we do not need to create a data loader to load a folder, we need to make inference to a single image
- [x] Structured API
- [x] Finish and test that everything works
- [x] Create logic about GPU (although not deploying with it).
- [ ] Deploy on Google Cloud without GPU, at least for now
- [x] Implement result image upload using Google Cloud Storage
- [ ] Publish API on RapidAPI

## Authors

- [Adrià Cabeza](https://github.com/adriacabeza)
- [Albert Suàrez](https://github.com/AlbertSuarez)

## License

Apache-2.0 © ObjectCut
