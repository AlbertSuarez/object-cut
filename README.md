# Engine: ⚙️ Core API of ObjectCut
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This repository contains all the logic necessary to run the ObjectCut Engine. It also contains a simple API to run the model. 

## Usage

### Setup
Build the image and spin up the container.
```bash
docker network create engine
docker-compose up -d --build
```
Run an image.
```bash
TODO
```

### API documentation
Go to http://localhost/docs


## Summary
- [x] Deleted data Loader from original U2Net: we do not need to create a data loader to load a folder, we need to make inference to a single image
- [x] Structured API
- [ ] Finish and test that everything works
- [ ] Create logic about GPU
- [ ] Set examples for the schemas and improve API documentation (in general)


