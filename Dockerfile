FROM python:3.8-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


RUN pip install --no-cache-dir -r requirements.txt
COPY ./src/ ./src/
CMD ["python", "./src/main.py"]