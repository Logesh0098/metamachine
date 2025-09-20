# Utility functions for file handling

def allowed_file(filename):
    return filename.endswith(('.jpeg', '.jpg', '.png', '.xlsx'))
import os
import tempfile
import streamlit as st

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary location and return the path"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def cleanup_file(file_path):
    """Delete a temporary file"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        st.error(f"Error cleaning up file: {str(e)}")
