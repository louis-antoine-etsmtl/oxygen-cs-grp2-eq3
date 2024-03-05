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
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Clean up unnecessary files and reduce the image size
RUN apk remove -y --purge build-essential && \
    apk autoremove -y && \
    apk clean && \
    rm -rf /var/lib/apt/lists/* /root/.cache /tmp/*

# Specify the command to run on container start
CMD ["python", "./src/main.py"]