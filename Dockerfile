### FIRST STAGE - RUNTIME BUILD ###

# Set base image
ARG BASE_IMAGE=python:3.11-slim
FROM $BASE_IMAGE AS runtime-image

# Optional field
LABEL maintainer="peter@gen7fuel.com"

# Install dependencies not present in the base image
RUN apt-get update && \
    apt-get install -y python3-dev && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy modules to install
COPY requirements.txt /tmp/requirements.txt
# Install modules
RUN pip install --no-cache --default-timeout=1200 -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# Set an internal user userId
ARG INTERNAL_UID=999
# Set an internal user groupId
ARG INTERNAL_GID=0
# Create the defined groupId, then add userId into groupId, and set home directory to /home/internal_docker
RUN groupadd -f -g ${INTERNAL_GID} internal_group && \
    useradd -m -d /home/internal_docker -s /bin/bash -g ${INTERNAL_GID} -u ${INTERNAL_UID} internal_docker

# Set app working directory
WORKDIR /app

# Create 
USER internal_docker

### SECOND STAGE - RUNTIME BUILD ###

# Set the image created in the first stage as the base image
FROM runtime-image

# Set the same userId as in runtime-image
ARG INTERNAL_UID=999
# Set the same groupId as in runtime-image
ARG INTERNAL_GID=0
# Copy whole project ensuring that the user has the same rights
COPY --chown=${INTERNAL_UID}:${INTERNAL_GID} . .

# Copy index.html to working directory
# COPY index.html /usr/local/lib/python3.10/site-packages/streamlit/static/index.html

# Choose port to expose
EXPOSE 8501

# Start the app
CMD [ "streamlit", "run" , "🏠_Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableWebsocketCompression=true", "--logger.level=info", "--server.enableXsrfProtection=false"]
