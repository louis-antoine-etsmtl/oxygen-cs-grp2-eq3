# Use a lightweight base image with Python
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /usr/src/app


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