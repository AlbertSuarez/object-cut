# Import base image
FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV HOME /srv/engine/multiplexer

# Set up configuration
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 8
ENV NGINX_MAX_UPLOAD 10m
ENV UWSGI_INI ${HOME}/uwsgi.ini

# Add needed files
ADD ./src ${HOME}/src
ADD ./requirements.lock ${HOME}/requirements.lock
ADD ./uwsgi.ini ${HOME}/uwsgi.ini

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r ${HOME}/requirements.lock

# Set up port to listen
ENV LISTEN_PORT 80
EXPOSE 80

# Move to working directory
WORKDIR ${HOME}
