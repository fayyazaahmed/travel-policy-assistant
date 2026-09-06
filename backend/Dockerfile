FROM python:3.11-slim

WORKDIR /app/backend

ENV PYTHONPATH=/app/backend

COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./
COPY frontend /app/frontend
COPY data /app/data

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]