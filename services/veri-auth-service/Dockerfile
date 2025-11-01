# ============================================
# VeriSyntra Auth Service - Dockerfile
# ============================================
# Multi-tenant authentication microservice
# Vietnamese PDPL 2025 Compliance Platform
# ============================================

FROM python:3.11-slim

# Set Vietnamese timezone
ENV TZ=Asia/Ho_Chi_Minh
ENV LANG=vi_VN.UTF-8
ENV LC_ALL=vi_VN.UTF-8

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    locales \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configure Vietnamese locale
RUN echo "vi_VN.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen vi_VN.UTF-8

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 veriauth && \
    chown -R veriauth:veriauth /app

# Copy application code
COPY --chown=veriauth:veriauth . .

# Switch to non-root user
USER veriauth

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Expose port
EXPOSE 8001

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--log-level", "info"]
