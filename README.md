# Engine: ⚙️ Core API of ObjectCut
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This repository contains all the logic necessary to run the ObjectCut Engine. It also contains a simple API to run the model. 

## Usage

### Setup
Download the models and put it in the data folder:
- https://drive.google.com/file/d/1rbSTGKAE-MTxBYHd-51l2hMOQPT_7EPy/view?usp=sharing
- https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view?usp=sharing

Build the image and spin up the container.

```bash
docker network create engine
docker-compose up -d --build
```
Run inference on an image.
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


