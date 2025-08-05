from fastapi import APIRouter
from models.task import tasks_db

router = APIRouter()

@router.get("/tasks")
async def get_tasks():
    return {"tasks": tasks_db}