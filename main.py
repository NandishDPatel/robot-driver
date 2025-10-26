import asyncio
import platform
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from automation_driver import RobotDriver
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="AutomationExercise Robot Driver API", version="1.0")

executor = ThreadPoolExecutor(max_workers=2) 
class TaskRequest(BaseModel):
    username: str
    password: str
    product: str

@app.get("/")
def root():
    return {"message": "AutomationExercise Robot API is running! Use POST /run-task to start automation."}

def run_robot_sync(username, password, product):
    """Run Playwright code safely in a new thread."""
    driver = RobotDriver()
    return asyncio.run(driver.run(username, password, product))

@app.post("/run-task")
async def run_task(request: TaskRequest):
    """
    Trigger the automation remotely.
    Example:
    POST /run-task
    {
        "username": "nanlogx@gmail.com",
        "password": "Login@12345",
        "product": "shirt"
    }
    """
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            executor, 
            run_robot_sync,
            request.username,
            request.password,
            request.product
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
