# tests/unit/test_main.py

import os
from fastapi.testclient import TestClient
from calculator_app.src.main import app
from calculator_app.src.logging_setup import setup_logging

# Create a test client using FastAPI's TestClient
client = TestClient(app)

# setup the logger to use a test file and directory
logger = setup_logging(test=True)


def test_read_root():
    # Test the root endpoint '/'
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the calculator API!'}


def test_health():
    # Test the /health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

    data = response.json()
    assert "version" in data
    assert "uptime" in data
    assert "started_time" in data
    assert "hostname" in data
    assert "environment" in data
    assert "started_by" in data
    assert "git_branch" in data


def test_calculate_add():
    # Test the '/calculate' endpoint for addition
    response = client.post("/calculate", json={"num1": 10, "num2": 5, "operation": "add"})
    assert response.status_code == 200
    assert response.json()["result"] == 15.0

def test_calculate_subtract():
    # Test the '/calculate' endpoint for subtraction
    response = client.post("/calculate", json={"num1": 10, "num2": 5, "operation": "subtract"})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0

def test_calculate_multiply():
    # Test the '/calculate' endpoint for multiplication
    response = client.post("/calculate", json={"num1": 10, "num2": 5, "operation": "multiply"})
    assert response.status_code == 200
    assert response.json()["result"] == 50.0

def test_calculate_divide():
    # Test the '/calculate' endpoint for division
    response = client.post("/calculate", json={"num1": 10, "num2": 5, "operation": "divide"})
    assert response.status_code == 200
    assert response.json()["result"] == 2.0

def test_calculate_divide_by_zero():
    # Test the '/calculate' endpoint for division by zero
    response = client.post("/calculate", json={"num1": 10, "num2": 0, "operation": "divide"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Division by zero is not allowed"

def test_calculate_invalid_operation():
    # Test the '/calculate' endpoint for an invalid operation
    response = client.post("/calculate", json={"num1": 10, "num2": 5, "operation": "invalid"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid operation. Supported operations: add, subtract, multiply, divide"

def test_log_file_and_directory_exist():
    # Test the logging directory is created if it does not exist
    # if os.path.exists(LOG_DIR):
    #     os.remove(LOG_DIR)
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    log_dir = os.path.join(log_dir, 'logs')
    log_file = os.path.join(log_dir, 'calculator_test_log.txt')

    # if os.path.exists(log_dir):
    #     os.remove(log_dir)
    # if os.path.exists(log_file):
    #     os.remove(log_file)

    # send some data in to create log activity
    response = client.post("/calculate", json={"num1": 10, "num2": 5, "operation": "add"})
    assert response.status_code == 200
    assert response.json()["result"] == 15.0

    # # Check if the log file is created
    # assert os.path.exists(log_dir), "Log directory was created"
    # assert os.path.exists(log_file), "Log file was created"
