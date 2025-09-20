

# --- Advanced UI for Streamlit Community Cloud ---
import streamlit as st
import pandas as pd
import numpy as np
import cv2
import tempfile
import os
from PIL import Image
import json
import matplotlib.pyplot as plt
from src.answer_key_parser import get_all_answer_keys
from src.database import OMRDatabase
from src.omr_grading_system import OMRGrader

st.set_page_config(
	page_title="OMR Grading System",
	page_icon="📝",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
	<style>
	.main {background-color: #f0f2f6;}
	.stButton>button {background-color: #ff4b4b; color: white;}
	.stFileUploader {background-color: #fff;}
	.stRadio label {font-weight: bold;}
	.stDownloadButton>button {background-color: #4bffb3; color: #31333f;}
	</style>
	""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=180)
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["🏠 Home", "📝 Grade Exam", "📊 Results History"])

# --- Home Page ---
if app_mode == "🏠 Home":
	st.title("📝 OMR Grading System")
	st.markdown("""
	<span style='color:#ff4b4b'><b>Welcome to the OMR Grading System!</b></span><br>
	<br>
	<ul>
	<li>Automatic OMR sheet detection and grading</li>
	<li>Support for both Set A and Set B exams</li>
	<li>Results stored in a database for future reference</li>
	<li>Visual feedback on graded sheets</li>
	<li>Detailed performance statistics</li>
	</ul>
	""", unsafe_allow_html=True)
	st.info("Use the sidebar to navigate between grading and results history.")
	# Show some statistics
	db = OMRDatabase()
	try:
		stats = db.get_stats()
		st.subheader("📈 System Statistics")
		col1, col2, col3, col4 = st.columns(4)
		col1.metric("Total Exams", stats['total_exams'])
		col2.metric("Average Score", f"{stats['avg_score']:.2f}%")
		col3.metric("Highest Score", f"{stats['max_score']:.2f}%")
		col4.metric("Lowest Score", f"{stats['min_score']:.2f}%")
	except:
		st.info("No exams processed yet. Process some exams to see statistics here.")

# --- Grade Exam Page ---
elif app_mode == "📝 Grade Exam":
	st.title("📝 Grade OMR Exam")
	st.markdown("""
	<span style='color:#4bffb3'><b>Upload your OMR sheet and select the exam set to begin grading.</b></span>
	""", unsafe_allow_html=True)
	uploaded_file = st.file_uploader("Upload OMR Sheet Image", type=["jpg", "jpeg", "png"], help="Accepted formats: jpg, jpeg, png")
	exam_set = st.radio("Select Exam Set", ("Set A", "Set B"))

	if uploaded_file is not None:
		image = Image.open(uploaded_file)
		st.image(image, caption="Uploaded OMR Sheet", use_column_width=True)
		st.success("File uploaded successfully! Now you can proceed to grading.")

		if st.button("Grade Exam", help="Click to grade the uploaded OMR sheet"):
			with st.spinner("Processing OMR sheet..."):
				with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
					tmp_file.write(uploaded_file.getvalue())
					tmp_path = tmp_file.name
				try:
					grader = OMRGrader("data/Key (Set A and B).xlsx")
					result = grader.process_omr_sheet(tmp_path, exam_set, save_results=False)
					st.session_state.processed = True
					st.session_state.result = result
					warped = cv2.imread(tmp_path)
					warped = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
					height, width = warped.shape[:2]
					cv2.putText(warped, f"Score: {result['score']:.2f}%", (width//2 - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
					st.session_state.graded_image = warped
					filename = uploaded_file.name
					db = OMRDatabase()
					db.save_exam_result(
						filename, exam_set, result['score'], result['correct'], result['total'], result['results']
					)
					st.success("Exam graded successfully!")
				except Exception as e:
					st.error(f"Error processing OMR sheet: {str(e)}")
				finally:
					os.unlink(tmp_path)

	if st.session_state.get('processed') and st.session_state.get('result'):
		result = st.session_state.result
		st.subheader("Results")
		col1, col2, col3 = st.columns(3)
		col1.metric("Score", f"{result['score']:.2f}%")
		col2.metric("Correct Answers", f"{result['correct']}/{result['total']}")
		col3.metric("Set", result['set'])
		if st.session_state.graded_image is not None:
			st.subheader("Graded OMR Sheet")
			st.image(st.session_state.graded_image, use_column_width=True)
		st.subheader("Detailed Results")
		detailed_data = []
		for q_num, res in result['results'].items():
			detailed_data.append({
				"Question": q_num,
				"Selected": res['selected'],
				"Correct": res['correct'],
				"Status": "Correct" if res['is_correct'] else "Incorrect"
			})
		df = pd.DataFrame(detailed_data)
		st.dataframe(df, use_container_width=True)
		json_result = json.dumps(result, indent=4)
		st.download_button(
			label="Download Results as JSON",
			data=json_result,
			file_name="omr_results.json",
			mime="application/json"
		)

# --- Results History Page ---
elif app_mode == "📊 Results History":
	st.title("📊 Results History")
	db = OMRDatabase()
	try:
		exams = db.get_all_exams()
		if not exams:
			st.info("No exams processed yet.")
		else:
			st.subheader("All Processed Exams")
			exam_data = []
			for exam in exams:
				exam_data.append({
					"ID": exam[0],
					"Filename": exam[1],
					"Set": exam[2],
					"Score": exam[3],
					"Correct": f"{exam[4]}/{exam[5]}",
					"Date": exam[6]
				})
			df = pd.DataFrame(exam_data)
			st.dataframe(df, use_container_width=True)
			st.subheader("Statistics")
			stats = db.get_stats()
			col1, col2, col3, col4 = st.columns(4)
			col1.metric("Total Exams", stats['total_exams'])
			col2.metric("Average Score", f"{stats['avg_score']:.2f}%")
			col3.metric("Highest Score", f"{stats['max_score']:.2f}%")
			col4.metric("Lowest Score", f"{stats['min_score']:.2f}%")
			st.subheader("Score Distribution")
			scores = [exam[3] for exam in exams]
			fig, ax = plt.subplots()
			ax.hist(scores, bins=10, edgecolor='black', alpha=0.7)
			ax.set_xlabel('Score (%)')
			ax.set_ylabel('Frequency')
			ax.set_title('Distribution of Exam Scores')
			st.pyplot(fig)
	except Exception as e:
		st.error(f"Error accessing database: {str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown("<center>OMR Grading System | Built with <a href='https://streamlit.io/' target='_blank'>Streamlit</a></center>", unsafe_allow_html=True)
