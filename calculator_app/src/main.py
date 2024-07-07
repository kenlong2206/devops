# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from calculator_app.src.logging_setup import setup_logging
from calculator_app.src.common import get_version, get_git_branch
from datetime import datetime
import os  # to run os commands
import socket  # to get hostname

# Set up logging
logger = setup_logging()

# Set start time as a global variable since it is set once when the application starts
start_time = datetime.now()

# Create FastAPI app
app = FastAPI()


# Define request body model
class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str


# Define routes
@app.get("/health")
def health():
    version = get_version('calculator_app')  # set in version.txt file
    git_branch = get_git_branch()
    current_time = datetime.now()
    uptime = current_time - start_time
    hostname = socket.gethostname()
    started_by = os.getenv('STARTED_BY', 'unknown_user')  # default to unknown_user if env variable not set

    health_info = {
        "status": "OK",
        "version": version,
        "uptime": str(uptime),
        "started_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": hostname,
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "started_by": started_by,
        "git_branch": git_branch
    }

    return health_info


@app.get("/")
def read_root():
    logger.info("Welcome message")
    return {"message": "Welcome to the calculator API!"}


@app.post("/calculate")
def calculate(request: CalculationRequest):
    num1 = request.num1
    num2 = request.num2
    operation = request.operation.lower()

    if operation == "add":
        logger.info("Add operation")
        result = num1 + num2
    elif operation == "subtract":
        logger.info("Subtract operation")
        result = num1 - num2
    elif operation == "multiply":
        logger.info("Multiply operation")
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            logger.warning("User error - divide by zero")
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        logger.info("Divide operation")
        result = num1 / num2
    else:
        logger.warning("User error - Invalid operation")
        raise HTTPException(status_code=400, detail="Invalid operation. Supported operations: add, subtract, multiply, divide")

    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
