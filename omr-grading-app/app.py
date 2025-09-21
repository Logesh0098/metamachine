


import streamlit as st
import os
import tempfile
import pandas as pd
from PIL import Image
import json
import matplotlib.pyplot as plt
import time
import random
from src.database import OMRDatabase

# Set page configuration
st.set_page_config(
    page_title="OMR Evaluation System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .subject-score {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .total-score {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Mock function to simulate OMR processing
def process_omr_sheet_mock(image_path, version):
    """Mock function to simulate OMR processing"""
    # Extract student ID from filename
    student_id = os.path.basename(image_path).split(".")[0]
    
    # Generate mock scores (in a real system, this would come from actual processing)
    total_score = random.randint(50, 95)
    
    # Generate subject scores that add up to total_score
    subject_scores = {}
    remaining = total_score
    subjects = ["Data Structures", "Algorithms", "Database", "Networking", "OS"]
    
    for i, subject in enumerate(subjects):
        if i == len(subjects) - 1:
            subject_scores[subject] = max(0, remaining)
        else:
            max_score = min(20, remaining - (len(subjects) - i - 1) * 10)
            min_score = min(15, max_score)
            if max_score < min_score:
                score = max_score
            else:
                score = random.randint(min_score, max_score)
            subject_scores[subject] = score
            remaining -= score
    
    # Generate mock answers
    answers = []
    for i in range(100):
        answers.append(random.choice(["A", "B", "C", "D"]))
    
    return {
        "student_id": student_id,
        "version": version,
        "total_score": total_score,
        "subject_scores": subject_scores,
        "answers": answers,
        "processing_time": f"{random.uniform(0.5, 2.5):.2f}s"
    }


# Initialize session state and database
if "results" not in st.session_state:
    st.session_state.results = []
    st.session_state.processed = False
if "db" not in st.session_state:
    st.session_state.db = OMRDatabase()

# App title and description
st.markdown('<h1 class="main-header">Automated OMR Evaluation System</h1>', unsafe_allow_html=True)
st.write("Upload OMR sheet images to automatically evaluate and score them.")


# Sidebar for navigation and settings
with st.sidebar:
    st.header("Settings")
    st.header("Upload OMR Sheets")
    uploaded_files = st.file_uploader(
        "Upload OMR sheet images",
        type=["jpeg", "jpg", "png"],
        accept_multiple_files=True
    )


# Process uploaded files and display results
if uploaded_files:
    st.session_state.results = []
    for uploaded_file in uploaded_files:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        # Call mock OMR processing (remove version argument)
        result = process_omr_sheet_mock(tmp_path, version=None)
        st.session_state.results.append(result)
        st.session_state.db.save_result(result)
        os.remove(tmp_path)

    st.session_state.processed = True

# Display results if processed
if st.session_state.processed and st.session_state.results:
    st.subheader("OMR Results")
    for result in st.session_state.results:
        st.markdown(f"<div class='score-card'><span class='total-score'>Student ID: {result['student_id']} | Total Score: {result['total_score']}</span></div>", unsafe_allow_html=True)
        st.write("Subject Scores:")
        for subject, score in result['subject_scores'].items():
            st.markdown(f"<span class='subject-score'>{subject}: {score}</span>", unsafe_allow_html=True)
