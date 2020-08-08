# Engine

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

⚙️ Core API of ObjectCut

This repository contains all the logic necessary to run the ObjectCut Engine. It also contains a simple API to run the model. 

## Usage

### Setup

Pull models from [Git LFS](https://git-lfs.github.com/)

```bash
git lfs fetch --all
```

Deploy the whole stuck (multiplexer, inference and traefik) with just this command.

```bash
docker-compose up -d --build --scale multiplexer=1 --scale inference=1
```

Run inference on an image.

```bash
curl --location --request POST 'localhost:80/remove' \
        --header 'Content-Type: application/json' \
        --header 'Host: multiplexer' \
        --header 'X-Secret-Access: SECRET' \
        --data-raw '{"image_url": IMAGE_URL}'
```


## Summary

- [x] Deleted data Loader from original U2Net: we do not need to create a data loader to load a folder, we need to make inference to a single image
- [x] Structured API
- [x] Finish and test that everything works
- [x] Create logic about GPU
- [ ] Deploy on Google Cloud with GPU
- [ ] Implement result image upload
