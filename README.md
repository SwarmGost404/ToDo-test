# Kanban Board - Quick Start

## Backend (FastAPI)
```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## FrontEnd (vue)
```bash
cd client
npm install
npm run dev -- --host
```
### And go for http://localhost:5173


## or use Docker
```bash
docker network create kanban
cd server
docker build -t kanban-client .
cd ../client
docker build -t kanban-api .
docker run -d -p 8080:8080 --network kanban --name kanban-client kanban-client
docker run -d -p 8000:8000 --network kanban --name kanban-api kanban-api
```

### And go for http://localhost:8080