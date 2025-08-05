from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import uuid
from datetime import datetime
import uvicorn

app = FastAPI()

# Хранение данных в памяти
tasks_db: List[Dict] = [
    {
        "id": str(uuid.uuid4()),
        "title": "Пример задачи",
        "description": "Это пример задачи в канбан-доске",
        "status": "todo",
        "createdAt": datetime.now().isoformat()
    }
]

# Хранение активных WebSocket соединений
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

    async def broadcast(self, message: Dict):
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                if message["type"] == "add-task":
                    new_task = {
                        "id": str(uuid.uuid4()),
                        "title": message["task"]["title"],
                        "description": message["task"]["description"],
                        "status": "todo",
                        "createdAt": datetime.now().isoformat()
                    }
                    tasks_db.append(new_task)
                    await manager.broadcast({
                        "type": "task-added",
                        "task": new_task
                    })
                    
                elif message["type"] == "move-task":
                    task_found = False
                    for task in tasks_db:
                        if task["id"] == message["taskId"]:
                            task["status"] = message["newStatus"]
                            task_found = True
                            await manager.broadcast({
                                "type": "task-moved",
                                "taskId": message["taskId"],
                                "newStatus": message["newStatus"]
                            })
                            break
                    
                    if not task_found:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Task with id {message['taskId']} not found"
                        })
                        
                elif message["type"] == "delete-task":
                    initial_length = len(tasks_db)
                    tasks_db[:] = [task for task in tasks_db if task["id"] != message["taskId"]]
                    
                    if len(tasks_db) < initial_length:
                        await manager.broadcast({
                            "type": "task-deleted",
                            "taskId": message["taskId"]
                        })
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Task with id {message['taskId']} not found"
                        })
                
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Unknown message type"
                    })
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })
            except KeyError as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Missing required field: {e}"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Unexpected error: {e}")
        manager.disconnect(websocket)

@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks_db}
