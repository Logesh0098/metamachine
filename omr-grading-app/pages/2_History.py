
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.database import OMRDatabase

st.set_page_config(page_title="Results History", page_icon="📊")

st.title("📊 Results History")

# Initialize database
@st.cache_resource
def init_database():
	return OMRDatabase()

db = init_database()

# Get all exams from database
try:
	exams = db.get_all_exams()
    
	if not exams:
		st.info("No exams processed yet.")
	else:
		# Display exams in a table
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
		st.dataframe(df)
        
		# Show statistics
		st.subheader("Statistics")
		stats = db.get_stats()
        
		col1, col2, col3, col4 = st.columns(4)
		col1.metric("Total Exams", stats['total_exams'])
		col2.metric("Average Score", f"{stats['avg_score']:.2f}%")
		col3.metric("Highest Score", f"{stats['max_score']:.2f}%")
		col4.metric("Lowest Score", f"{stats['min_score']:.2f}%")
        
		# Create a score distribution chart
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
