# Базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY reqirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r reqirements.txt

# Копируем весь проект
COPY . .

# Открываем порт, который использует FastAPI (обычно 8000)
EXPOSE 8000

# Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]