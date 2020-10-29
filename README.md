<br>
<p align="center">
  <img alt="ObjectCut" src="docs/images/object-cut.png" width="50%"/>
</p>
<br>

[![HitCount](http://hits.dwyl.io/AlbertSuarez/object-cut.svg)](http://hits.dwyl.io/AlbertSuarez/object-cut)
[![ObjectCut Uptime in the last 30 days](https://objectcut.com)](https://img.shields.io/uptimerobot/ratio/m785761556-2b6dc04bab1e70dd48e49042)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/AlbertSuarez/object-cut)
[![GitHub stars](https://img.shields.io/github/stars/AlbertSuarez/object-cut.svg)](https://GitHub.com/AlbertSuarez/object-cut/stargazers/)
[![GitHub forks](https://img.shields.io/github/forks/AlbertSuarez/object-cut.svg)](https://GitHub.com/AlbertSuarez/object-cut/network/)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/AlbertSuarez/object-cut.svg)](https://github.com/AlbertSuarez/object-cut)

✂️ Cut the main object of an image automagically

This repository contains all the logic necessary to run the ObjectCut Engine. It also contains a simple API to run the model. 

## Requirements

1. Python 3.7+
2. Docker CE
3. Docker-compose

## Recommendations

Usage of [virtualenv](https://realpython.com/blog/python/python-virtual-environments-a-primer/) is recommended for package library / runtime isolation.

## Usage

To run the server, please execute the following from the root directory:

1. Set up environment creating the `.env` file. This file must have this structure (without the brackets):

    ```
    SECRET_ACCESS={SECRET_ACCESS}
    ```

2. Set up your Google Cloud Storage credentials, decrypt it using GPG with the needed passphrase and decompress it:

    ```bash
    gpg --quiet --batch --yes --decrypt --passphrase="{{ GPG_PASSPHRASE }}" \
            --output ./multiplexer/keys/storage_key.tar ./multiplexer/keys/storage_key.tar.gpg
    tar xvf ./multiplexer/keys/storage_key.tar -C ./multiplexer/keys
    ```

3. Build everything in parallel:

    ````bash
   docker-compose build --parallel 
   ````

4. Deploy the whole stuck (multiplexer, inference and traefik) with just this command.

    ```bash
    docker-compose up -d --scale multiplexer=1 --scale inference=3
    ```

_That's it_! You have ObjectCut running on port 80 routing traffic using _traefik_.

## Run tests

1. Run ObjectCut locally

2. Move to multiplexer module

    ```bash
    cd multiplexer
    ```

3. Run tests

    ```bash
    SECRET_ACCESS={SECRET_ACCESS} python3 -m unittest discover -v
    ```

## Development

### Integrations

This API integrates with several external APIs which are listed below.

#### Google Cloud Storage

For being able to upload the image response to a public bucket for let the users download the output, we are using GCS for doing it once the users specify that in the `output_format=url` (default value) in the API request.

The integration is pretty simple. Every request is being authenticated using the service account JSON file under the `multiplexer/keys` folder where every output image is being upload to the `object-cut-images` bucket under a Life Cycle policy of *3 days* (this has been configured on the Google Cloud Console UI). Once the file has been uploaded (and make it public) the library itself it returns you the public URL that you can return to the user.

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

## Authors

- [Adrià Cabeza](https://github.com/adriacabeza)
- [Albert Suàrez](https://github.com/AlbertSuarez)

## License

Apache-2.0 © ObjectCut
