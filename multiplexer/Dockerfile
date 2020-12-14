# Import base image
FROM python:3.7
ENV HOME /srv/engine/multiplexer

# Add needed files
ADD ./keys ${HOME}/keys
ADD ./src ${HOME}/src
ADD ./requirements.lock ${HOME}/requirements.lock
ADD ./uwsgi.ini ${HOME}/uwsgi.ini

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r ${HOME}/requirements.lock
RUN pip uninstall --yes Pillow; exit 0
RUN CC='cc -mavx2' pip install --upgrade --force-reinstall Pillow-SIMD==7.0.0.post3

# Move to working directory
WORKDIR ${HOME}

# Comand
CMD uwsgi --ini uwsgi.ini
