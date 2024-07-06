# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -v --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Create a volume to persist logs
VOLUME ["/app/logs"]

# Ensure the log directory and file exist and set appropriate permissions
RUN mkdir -p /app/logs && touch /app/logs/calculator_log.txt && chmod -R 777 /app/logs

# Define environment variable
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Expose the port your app runs on (if applicable)
EXPOSE 8000

# Command to run your application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
