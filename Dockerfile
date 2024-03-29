FROM python:3.8 as build

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.8-slim as runtime

WORKDIR /usr/src/app
COPY ./src/ ./src/


CMD ["python", "./src/main.py"]