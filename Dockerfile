# Stage 1: Build
FROM python:3.8 as build

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.8-slim as runtime

COPY --from=build /opt/venv /opt/venv

WORKDIR /usr/src/app

ENV PATH="/opt/venv/bin:$PATH"


CMD ["python", "./src/main.py"]