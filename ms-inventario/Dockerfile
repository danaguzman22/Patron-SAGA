FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn --no-cache-dir

EXPOSE 5003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5003"]
