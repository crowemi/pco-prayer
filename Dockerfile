FROM python:3.8-slim

# Update and install system packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y -q \
    gcc libpq-dev python-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY main.py requirements.txt ./

RUN python -m pip install --no-cache-dir --prefer-binary --upgrade --user \
    -r requirements.txt 

ENTRYPOINT [ "sh" ]
