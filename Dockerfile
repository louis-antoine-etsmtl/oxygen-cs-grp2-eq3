FROM alpine AS compile-image

RUN apk add --no-cache python3 py-pip openssl ca-certificates python3-dev build-base wget

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python3 -m venv /usr/src/app
RUN /usr/src/app/bin/pip install -r requirements.txt

FROM alpine AS runtime-image

RUN apk add --no-cache python3 openssl ca-certificates

WORKDIR /usr/src/app
COPY . /usr/src/app

COPY --from=compile-image /usr/src/app/ ./

CMD ["python", "./src/main.py"]