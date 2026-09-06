FROM python:3.11-slim

WORKDIR /app/backend

ENV PYTHONPATH=/app/backend

COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./
COPY frontend /app/frontend
COPY data /app/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]