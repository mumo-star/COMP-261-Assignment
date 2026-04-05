# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose Streamlit port as main service
EXPOSE 8501

# Health check for Streamlit frontend
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Start FastAPI in background, then Streamlit as main process
CMD ["sh", "-c", "streamlit cache clear && python -m uvicorn main:app --host 0.0.0.0 --port 8001 > /dev/null 2>&1 & sleep 3 && streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false"]
