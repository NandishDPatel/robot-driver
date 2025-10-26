import asyncio
import platform
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from automation_driver import RobotDriver

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="AutomationExercise Robot Driver API", version="1.0")


class TaskRequest(BaseModel):
    username: str
    password: str
    product: str


@app.get("/")
def root():
    return {"message": "AutomationExercise Robot API is running! Use POST /run-task to start automation."}

@app.post("/run-task")
async def run_task(request: TaskRequest):
    """
    Trigger the automation remotely.
    Example:
    POST /run-task
    {
        "username": "nanlogx@gmail.com",
        "password": "Login@12345",
        "product": "dress"
    }
    """
    try:
        driver = RobotDriver()
        result = await driver.run(request.username, request.password, request.product)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    