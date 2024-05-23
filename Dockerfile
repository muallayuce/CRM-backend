FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG PIP_EXTRA_INDEX_URL

WORKDIR /app

# Install dependencies
COPY requirements.txt /app

RUN apt update && \
    apt install -y git ruby-dev ruby-ffi postgresql-client redis-server wkhtmltopdf && \
    apt clean && \
    gem install sass && \
    gem install compass && \
    apt install -y nodejs npm && \
    npm install -g less && \
    apt install -y python3-pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt && \
    python3 -m pip install --no-cache-dir redis

COPY . /app

COPY entrypoint.sh /app/entrypoint.sh
COPY wait-for-postgres.sh /app/wait-for-postgres.sh

RUN chmod +x /app/entrypoint.sh /app/wait-for-postgres.sh

ENTRYPOINT ["./entrypoint.sh"]
