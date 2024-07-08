# tests/unit/test_main.py

import os
from fastapi.testclient import TestClient
from src.main import app
from src.log import setup_logging

# Create a test client using FastAPI's TestClient
client = TestClient(app)

# setup the logger to use a test file and directory
logger = setup_logging(test=True)



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

