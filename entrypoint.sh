#!/bin/bash

# Clear Streamlit cache
streamlit cache clear

# Start FastAPI in background
python -m uvicorn main:app --host 0.0.0.0 --port 8001 > /dev/null 2>&1 &

# Wait a moment for FastAPI to start
sleep 3

# Start Streamlit as main process (this will be what Render detects)
exec streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false
