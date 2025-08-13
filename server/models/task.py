from typing import Dict, List
import uuid
from datetime import datetime

tasks_db: List[Dict] = [
    {
        "id": str(uuid.uuid4()),
        "title": "Пример задачи",
        "description": "Это пример задачи в канбан-доске",
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "color": "status-none"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Пример задачи",
        "description": "Это пример задачи в канбан-доске",
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "color": "status-red"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Пример задачи",
        "description": "Это пример задачи в канбан-доске",
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "color": "status-green"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Пример задачи",
        "description": "Это пример задачи в канбан-доске",
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "color": "status-yellow"
    }
]