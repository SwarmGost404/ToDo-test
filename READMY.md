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

## Or user docker
```bash
docker run -d -p 8000:8000 --name kanban-api kanban-api
docker run -d -p 8080:8080 --name kanban-client kanban-client
```