from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import httpx
import random
from common.src.log import setup_logging
from common.src.healthcheck import get_version, get_git_branch
import socket
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Determine the base directory dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# get the URL for the calculator_app service from the environment variable set in the docker-compose file
# if the environment variable is not set use the default localhost
CALCULATOR_URL = os.getenv("CALCULATOR_URL", "http://127.0.0.1:8000")

# Set up logging
logger = setup_logging(app_name='client_app')

# Create FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global variables
sending_sums = False
delay = 1
operations = ['add', 'subtract', 'multiply', 'divide']
results = []

# Set start time as a global variable since it is set once when the application starts
start_time = datetime.now()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": results})

@app.post("/start")
async def start_sending():
    global sending_sums
    sending_sums = True
    logger.info("Started sending sums to calculator_app")
    return {"status": "started"}

@app.post("/stop")
async def stop_sending():
    global sending_sums
    sending_sums = False
    logger.info("Stopped sending sums to calculator_app")
    return {"status": "stopped"}

@app.post("/reset")
async def reset():
    global results
    results = []
    logger.info("Reset results list")
    return {"status": "reset"}

@app.post("/set_delay")
async def set_delay(new_delay: float = Form(...)):
    global delay
    delay = new_delay
    logger.info(f"Set delay between sums to {delay} seconds")
    return {"status": "delay set", "delay": delay}

@app.post("/send_sums")
async def send_sums():
    calculator_url = CALCULATOR_URL
    num1 = random.randint(0, 1000)
    num2 = random.randint(0, 1000)
    operation = random.choice(operations)
    logger.info(f"Received send_sums request: num1={num1}, num2={num2}, operation={operation}")
    request_url = f"{calculator_url}/calculate"
    logger.info(f"Sending request to: {request_url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{calculator_url}/calculate",
                json={"num1": num1, "num2": num2, "operation": operation}
            )
            result = response.json().get("result")
            logger.info(f"Forwarded request to calculator_app: status={response.status_code}, result={result}")
            return {
                "Num1": num1,
                "Num2": num2,
                "Operation": operation,
                "Result": result
            }
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise HTTPException(status_code=500, detail="Error processing request")
        except Exception as e:
            logger.error(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error processing request")

@app.get("/health")
def health():
    logger.info("Health-check")
    version = get_version('client_app')  # set in version.txt file
    current_time = datetime.now()
    uptime = current_time - start_time
    hostname = socket.gethostname()
    started_by = os.getenv('STARTED_BY', 'unknown_user')  # default to unknown_user if env variable not set

    if started_by == "docker":
        host = "docker_container_id"
        git_branch = "n/a"
    else:
        host = "hostname"
        git_branch = get_git_branch()

    health_info = {
        "status": "OK",
        "app_name": "client_app",
        "version": version,
        "uptime": str(uptime),
        "started_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "started_by": started_by,
        "git_branch": git_branch,
        host: hostname
    }

    return health_info

@app.get("/results", response_class=JSONResponse)
async def get_results():
    return {"results": results}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
