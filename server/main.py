from fastapi import FastAPI
from routers import tasks, websocket

app = FastAPI()

app.include_router(tasks.router)
app.include_router(websocket.router)