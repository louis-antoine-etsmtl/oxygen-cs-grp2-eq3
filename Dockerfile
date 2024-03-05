# Use a lightweight base image with Python
FROM python:alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /usr/src/app


# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

# Install dependencies
COPY requirements.txt ./
RUN apk --no-cache add \
    build-base \
    libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base libffi-dev

# Copy the application code into the container
COPY . .

# Specify the command to run on container start
CMD ["python", "./src/main.py"]