# Stage 1: Build
FROM python:3.8 as build

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.8-slim as runtime

WORKDIR /usr/src/app
COPY --from=build /usr/src/app /usr/src/app

# Cleanup unnecessary files and reduce the image size
RUN apt-get remove -y --purge build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /root/.cache /tmp/*

CMD ["python", "./src/main.py"]