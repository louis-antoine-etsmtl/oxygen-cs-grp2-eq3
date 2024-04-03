FROM python:3.8.10-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./

# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev


RUN pip install --no-cache-dir -r requirements.txt
COPY ./src/ ./src/
CMD ["python", "./src/main.py"]