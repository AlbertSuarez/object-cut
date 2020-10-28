# Import base image
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME /srv/engine/inference

# Install dependencies
RUN apt-get update   
RUN apt-get install -y --no-install-recommends \
	software-properties-common \
	build-essential \
	cmake \
	git \
	wget \
	libatlas-base-dev \
	libboost-all-dev \
	libgflags-dev \
	libgoogle-glog-dev \
	libhdf5-serial-dev \
	libleveldb-dev \
	liblmdb-dev \
	libopencv-dev \
	libprotobuf-dev \
	libsnappy-dev \
	protobuf-compiler \
	libnvinfer5

# Environment variable to avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1 

# Install Python3.7
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update
RUN apt-get install -y \
	python3.7 \
	python3-dev \
	python3-setuptools \
	python3-pip
ENV PYTHON_VERSION=3.7

# Add needed files
ADD ./data ${HOME}/data
ADD ./src ${HOME}/src
ADD ./gdrive_download.sh ${HOME}/gdrive_download.sh
ADD ./requirements.lock ${HOME}/requirements.lock

# Download models
RUN ${HOME}/gdrive_download.sh 1s52ek_4YTDRt_EOkx1FS53u-vJa0c4nu ${HOME}/data/basnet.pth
RUN ${HOME}/gdrive_download.sh 1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ ${HOME}/data/u2net.pth
RUN ${HOME}/gdrive_download.sh 1rbSTGKAE-MTxBYHd-51l2hMOQPT_7EPy ${HOME}/data/u2netp.pth

# Install dependencies
RUN python3 -m pip install pip --upgrade
RUN pip3 install --upgrade --force-reinstall wheel
RUN pip3 install -r ${HOME}/requirements.lock && rm -rf /root/.cache/pip
RUN pip3 uninstall --yes Pillow; exit 0
RUN CC='cc -mavx2' pip3 install --upgrade --force-reinstall Pillow-SIMD==7.0.0.post3

# UTF-8 support
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set up port to listen from Traefik
EXPOSE 80

# Move to working directory
WORKDIR ${HOME}

# Comand
CMD uvicorn src.main:app --host 0.0.0.0 --port 80
