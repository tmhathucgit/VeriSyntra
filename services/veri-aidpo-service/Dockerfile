# VeriAIDPO Classification Service Dockerfile
# Base image: Python 3.13-slim for smaller image size
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY main.py .

# Create model cache directory
RUN mkdir -p /app/models

# Expose port
EXPOSE 8001

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
