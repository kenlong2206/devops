# tests/unit/test_main.py
from fastapi.testclient import TestClient
from client_app.src.main import app
from common.src.log import setup_logging
from unittest.mock import patch, Mock
import requests


# Create a test client using FastAPI's TestClient
client = TestClient(app)

# setup the logger to use a test file and directory
logger = setup_logging(test=True, app_name='client_app')


def test_read_root():
    # Test the root endpoint '/'
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>sum sender</title>" in response.text.lower()


def test_health():
    # Test the /health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

    data = response.json()
    assert "version" in data
    assert response.json()["app_name"] == "client_app"
    assert "uptime" in data
    assert "started_time" in data
    assert "hostname" in data
    assert "environment" in data
    assert "started_by" in data
    assert "git_branch" in data


def test_start_sending():
    response = client.post("/start")
    assert response.status_code == 200
    assert response.json() == {'status': 'started'}


def test_stop_sending():
    response = client.post("/stop")
    assert response.status_code == 200
    assert response.json() == {'status': 'stopped'}


def test_reset():
    response = client.post("/reset")
    assert response.status_code == 200
    assert response.json() == {'status': 'reset'}


def test_set_delay():
    response = client.post("/set_delay", data={"new_delay": 2})
    assert response.status_code == 200
    assert response.json() == {"status": "delay set", "delay": 2}


# Mocking the requests.post call in send_sums
# @patch('requests.post')
# def test_send_sums(mock_post):
#     # setup mock function to mock /calculate
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {
#         "Num1": 1,
#         "Num2": 2,
#         "Operation": "add",
#         "Result": 4
#     }
#     mock_post.return_value = mock_response
#
#     # call the function
#     response = client.post("/send_sums")
#
#     # check response
#     assert response.status_code == 200
#     data = response.json()
#     assert "Num1" in data
#     assert "Num2" in data
#     assert "Operation" in data
#     assert "Result" in data
#
#     # check the random sum gets the right answer
#     if data["Operation"] == "add":
#         test_result = data["Num1"] + data["Num2"]
#     elif data["Operation"] == "subtract":
#         test_result = data["Num1"] - data["Num2"]
#     if data["Operation"] == "multiply":
#         test_result = data["Num1"] * data["Num2"]
#     if data["Operation"] == "divide":
#         test_result = data["Num1"] / data["Num2"]
#
#     assert data["Result"] == test_result
