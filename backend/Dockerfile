# ============================================
# VeriSyntra FastAPI Backend - Production Dockerfile
# ============================================
# Multi-stage build for Vietnamese PDPL 2025 Compliance Platform
# Supports: PhoBERT models, Vietnamese NLP, Hugging Face Hub integration
# ============================================

# ============================================
# Stage 1: Base Image with System Dependencies
# ============================================
FROM python:3.11-slim as base

# Set Vietnamese timezone
ENV TZ=Asia/Ho_Chi_Minh
ENV LANG=vi_VN.UTF-8
ENV LC_ALL=vi_VN.UTF-8

# Install system dependencies for Vietnamese NLP and PDF processing
RUN apt-get update && apt-get install -y \
    # Vietnamese locale support
    locales \
    # Tesseract OCR for Vietnamese document processing
    tesseract-ocr \
    tesseract-ocr-vie \
    # PDF processing libraries
    libmupdf-dev \
    mupdf-tools \
    # Network utilities
    curl \
    wget \
    # Build dependencies
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Configure Vietnamese locale
RUN echo "vi_VN.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen vi_VN.UTF-8

# ============================================
# Stage 2: Python Dependencies
# ============================================
FROM base as dependencies

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies with caching
# Use --no-cache-dir to reduce image size
# Use --prefer-binary for faster installs
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# ============================================
# Stage 3: Application Layer
# ============================================
FROM dependencies as application

# Create non-root user for security
RUN useradd -m -u 1000 verisyntra && \
    mkdir -p /app /app/logs /app/cache && \
    chown -R verisyntra:verisyntra /app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=verisyntra:verisyntra . .

# Create directories for model cache and logs
RUN mkdir -p /app/app/ml/models /app/logs /app/cache && \
    chown -R verisyntra:verisyntra /app/app/ml/models /app/logs /app/cache

# Switch to non-root user
USER verisyntra

# Environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Hugging Face Hub configuration
# Models will be downloaded to /app/cache/huggingface
ENV HF_HOME=/app/cache/huggingface
ENV TRANSFORMERS_CACHE=/app/cache/huggingface/transformers
ENV HF_DATASETS_CACHE=/app/cache/huggingface/datasets

# FastAPI/Uvicorn configuration
ENV PORT=8000
ENV HOST=0.0.0.0
ENV WORKERS=1

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Expose port
EXPOSE ${PORT}

# ============================================
# Startup Command
# ============================================
# Use uvicorn with:
# - Auto-reload disabled in production
# - Single worker (scale with container orchestration)
# - Proper host binding for container networking
# - Graceful shutdown support

CMD ["uvicorn", "main_prototype:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--log-level", "info", \
     "--access-log", \
     "--use-colors"]

# ============================================
# Build Instructions
# ============================================
# Build: docker build -t verisyntra-backend:latest .
# Run:   docker run -d -p 8000:8000 \
#          -e HF_TOKEN=your_hf_token \
#          -e DATABASE_URL=postgresql://... \
#          --name verisyntra-backend \
#          verisyntra-backend:latest
#
# Development: docker run -d -p 8000:8000 \
#          -v $(pwd):/app \
#          -e HF_TOKEN=your_hf_token \
#          verisyntra-backend:latest
# ============================================

# ============================================
# Image Labels (OCI Standard)
# ============================================
LABEL org.opencontainers.image.title="VeriSyntra Backend"
LABEL org.opencontainers.image.description="Vietnamese PDPL 2025 Compliance Platform - FastAPI Backend"
LABEL org.opencontainers.image.version="1.0.0-prototype"
LABEL org.opencontainers.image.vendor="VeriSyntra"
LABEL org.opencontainers.image.authors="VeriSyntra Development Team"
LABEL maintainer="VeriSyntra Team"
LABEL verisyntra.service.name="verisyntra-monolith"
LABEL verisyntra.service.type="fastapi-backend"
LABEL verisyntra.language="Vietnamese"
LABEL verisyntra.compliance="PDPL-2025"
