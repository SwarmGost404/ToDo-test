from fastapi import WebSocket
from typing import List
from datetime import datetime
from models.task import tasks_db

active_connections: List[WebSocket] = []

class ConnectionManager:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        active_connections.append(websocket)
        await self.send_initial_data(websocket)

    def disconnect(self, websocket: WebSocket):
        active_connections.remove(websocket)

    async def send_initial_data(self, websocket: WebSocket):
        await websocket.send_json({
            "type": "initial-data",
            "tasks": tasks_db
        })

    async def broadcast(self, message: dict):
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)