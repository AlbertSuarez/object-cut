FROM python:3.8.1


WORKDIR /usr/src/engine

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# environment variable to avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1 

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# PILLOW
#RUN pip3 uninstall --yes Pillow; exit 0
#RUN CC="cc -mavx2" pip3 install --upgrade --force-reinstall Pillow-SIMD==7.0.0.post3

# copy project
COPY . /usr/src/app/
