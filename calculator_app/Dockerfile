# NOTE: docker images created as /devops level to *_app and common can be included

# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY calculator_app/requirements.txt /app/calculator_app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/calculator_app/requirements.txt

# Copy the entire project into the container
COPY calculator_app /app/calculator_app
COPY common /app/common
COPY tests /app/tests

# Create a volume to persist logs
VOLUME ["/app/calculator_app/logs"]

# Ensure the log directory and file exist and set appropriate permissions
RUN mkdir -p /app/calculator_app/logs && touch /app/calculator_app/logs/calculator_app_log.txt && chmod -R 777 /app/calculator_app/logs

# Define environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.:/app:/app/calculator_app:/app/calculator_app/src:/app/common/src:/app/common/
ENV STARTED_BY=docker
ENV baseCalculatorUrl=http://127.0.0.1:9000

# Expose the port your app runs on (if applicable)
EXPOSE 8000

# Command to run your application
CMD ["uvicorn", "calculator_app.src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
