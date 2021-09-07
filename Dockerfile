FROM python:3.8-slim

# Update and install system packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y -q \
    gcc libpq-dev python-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV APPDIR=/app

# Create the app dir and set permissions
RUN mkdir $APPDIR

# migrate the app
WORKDIR $APPDIR

COPY main.py run.sh requirements.txt ./

RUN pip3 install -r requirements.txt 

ENTRYPOINT [ "/bin/bash", "./run.sh" ]
# ENTRYPOINT [ "sh" ]
