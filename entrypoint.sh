#!/bin/bash

# Clear Streamlit cache
streamlit cache clear

# Start ONLY Streamlit (no FastAPI)
exec streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false
