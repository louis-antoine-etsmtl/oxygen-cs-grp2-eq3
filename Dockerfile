# Use a slim base image for smaller size
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ src/

# Run the application
CMD ["python", "./src/main.py"]