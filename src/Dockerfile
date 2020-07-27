FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/engine

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN apt-get update   
RUN apt-get install -y --no-install-recommends \
	software-properties-common \
	build-essential \
	python3 \
	python3-dev \
	python3-pip \
	python3-setuptools \
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

# environment variable to avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1 

RUN python3 -m pip install pip --upgrade
RUN pip3 install --upgrade --force-reinstall wheel
RUN pip3 install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# PILLOW
#RUN pip3 uninstall --yes Pillow; exit 0
#RUN CC="cc -mavx2" pip3 install --upgrade --force-reinstall Pillow-SIMD==7.0.0.post3

# copy project
COPY . /usr/src/app/
