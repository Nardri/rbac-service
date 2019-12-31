ARG PYTHON_VERSION=3.7-slim

# Set base image
FROM python:${PYTHON_VERSION}

# Set maintainer
LABEL maintainer='Victor Nwokeocha'

# Python unbuffered env and python dont write byte code variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade and install pipenv
RUN pip install --upgrade pip && pip install pipenv

WORKDIR /usr/src/app

# creation of requirements.txt
COPY ./Pipfile* ./

# Install dependencies
RUN pipenv lock -r > requirements.txt \
    && pip install -r ./requirements.txt

RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Copy all the files from local to docker
COPY ./ ./

RUN chmod +x ./Docker/entrypoint.sh

# Create a user to run the app on docker
RUN useradd -r -u 1234 -U docker-user

# Change the ownership of the working dir to the new user
# and give write access to the folder.
RUN chown -R docker-user:docker-user ./ \
    && chmod 755 ./

# Switch to the new user
USER docker-user

CMD sh ./Docker/entrypoint.sh

EXPOSE 5000
