# NOTE: docker images created as /devops level to *_app and common can be included

# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY client_app/requirements.txt /app/client_app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/client_app/requirements.txt

# Copy the entire project into the container
COPY client_app /app/client_app
COPY common /app/common

# Create a volume to persist logs
VOLUME ["/app/client_app/logs"]

# Ensure the log directory and file exist and set appropriate permissions
RUN mkdir -p /app/client_app/logs && touch /app/client_app/logs/client_log.txt && chmod -R 777 /app/client_app/logs

# Define environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.:/app:/app/client_app:/app/client_app/src:/app/common/src
ENV STARTED_BY=docker

# Expose the port your app runs on (if applicable)
EXPOSE 9000

# Command to run your application
CMD ["uvicorn", "client_app.src.main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
