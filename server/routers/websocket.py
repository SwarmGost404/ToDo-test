from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from managers.connection_manager import ConnectionManager
from models.task import tasks_db
import uuid
from datetime import datetime

manager = ConnectionManager()

router = APIRouter()

@router.websocket("/ws")
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
                
                elif message["type"] == "edit-task":
                    task_found = False
                    for task in tasks_db:
                        if task["id"] == message["taskId"]:
                            # Обновляем поля задачи
                            task["title"] = message["updates"].get("title", task["title"])
                            task["description"] = message["updates"].get("description", task["description"])
                            task["updatedAt"] = datetime.now().isoformat()
                            
                            task_found = True
                            await manager.broadcast({
                                "type": "task-updated",
                                "taskId": message["taskId"],
                                "updates": {
                                    "title": task["title"],
                                    "description": task["description"],
                                    "updatedAt": task["updatedAt"]
                                }
                            })
                            break
                    
                    if not task_found:
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
    except Exception:
        manager.disconnect(websocket)