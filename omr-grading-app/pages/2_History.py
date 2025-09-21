
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.database import OMRDatabase

st.set_page_config(page_title="Results History", page_icon="📊")

st.title("📊 Results History")


# Use shared database from session state
if "db" not in st.session_state:
	st.session_state.db = OMRDatabase()
db = st.session_state.db

# Get all exams from database
try:
	exams = db.get_all_exams()
	if not exams:
		st.info("No exams processed yet.")
	else:
		st.subheader("All Processed Exams")
		exam_data = []
		for exam in exams:
			exam_data.append({
				"Student ID": exam.get("student_id", "-"),
				"Score": exam.get("total_score", "-"),
				"Subjects": ", ".join([f"{sub}: {score}" for sub, score in exam.get("subject_scores", {}).items()]),
				"Processing Time": exam.get("processing_time", "-")
			})
		df = pd.DataFrame(exam_data)
		st.dataframe(df)
		# Score distribution
		st.subheader("Score Distribution")
		scores = [exam.get("total_score", 0) for exam in exams]
		fig, ax = plt.subplots()
		ax.hist(scores, bins=10, edgecolor='black', alpha=0.7)
		ax.set_xlabel('Score')
		ax.set_ylabel('Frequency')
		ax.set_title('Distribution of Exam Scores')
		st.pyplot(fig)
except Exception as e:
	st.error(f"Error accessing database: {str(e)}")
