# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from client_app.src.log import setup_logging
from client_app.src.healthcheck import get_version, get_git_branch
from datetime import datetime
import os  # to run os commands
import socket  # to get hostname

# Set up logging
logger = setup_logging()

# Set start time as a global variable since it is set once when the application starts
start_time = datetime.now()

# Create FastAPI app
app = FastAPI()



# Define routes
@app.get("/health")
def health():
    logger.info("Health-check")
    version = get_version('client_app')  # set in version.txt file
    git_branch = get_git_branch()
    current_time = datetime.now()
    uptime = current_time - start_time
    hostname = socket.gethostname()
    started_by = os.getenv('STARTED_BY', 'unknown_user')  # default to unknown_user if env variable not set

    health_info = {
        "status": "OK",
        "app_name": "client_app",
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
    return {"message": "Welcome to the client API!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=9000)
