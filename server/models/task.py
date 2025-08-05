from typing import Dict, List
import uuid
from datetime import datetime

tasks_db: List[Dict] = [
    {
        "id": str(uuid.uuid4()),
        "title": "Пример задачи",
        "description": "Это пример задачи в канбан-доске",
        "status": "todo",
        "createdAt": datetime.now().isoformat()
    }
]