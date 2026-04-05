
import streamlit as st
import requests

def get_api_base_url():
    """
    Returns the base URL for API endpoints.
    Configured for local development.
    
    Returns:
        str: Base URL for the backend API
    """
    return "http://localhost:8001"

def get_auth_headers():
    """
    Returns authentication headers for API requests.
    Currently returns empty headers as no authentication is required.
    
    Returns:
        dict: Dictionary of authentication headers
    """
    #No authentication required - return empty headers
    return {}

def handle_api_error(response):
    """
    Handles API error responses with user-friendly messages.
    Provides appropriate feedback based on status code.
    
    Args:
        response: HTTP response object from requests library
    """
    if response.status_code == 401:
        st.error("Authentication error - but no auth required in this version")
    elif response.status_code == 403:
        st.error("Permission denied")
    elif response.status_code == 404:
        st.error("Resource not found")
    elif response.status_code == 500:
        st.error("Server error - please try again later")
    else:
        try:
            error_data = response.json()
            st.error(f"Error: {error_data.get('detail', 'Unknown error')}")
        except:
            st.error(f"Error: {response.status_code} - {response.text}")
