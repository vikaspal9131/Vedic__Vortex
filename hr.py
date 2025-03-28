import sqlite3
import streamlit as st
from resumeAnalysis import analyze_and_store_resumes, get_analyzed_resumes, get_job_descriptions

DB_PATH = "resumes.db"

# ✅ Save new job description to database
def save_job_description(description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_descriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT)''')
    cursor.execute("INSERT INTO job_descriptions (description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

# ✅ Display job description input form
def show_job_role_specification():
    st.title("📝 Job Role Specification")

    # Input field for job description
    job_description = st.text_area("Enter Job Description:", height=200)

    if st.button("Save Job Description"):
        if job_description.strip():
            save_job_description(job_description)
            st.success("✅ Job description saved successfully!")
        else:
            st.warning("⚠ Please enter a valid job description.")

# ✅ Show HR Dashboard Analysis
def show_hr_dashboard_analysis():
    st.title("📊 HR Dashboard Analysis")

    job_descriptions = get_job_descriptions()
    
    if not job_descriptions:
        st.warning("⚠ No job descriptions found. Please add one first.")
        return

    selected_job = st.selectbox("Select a Job Description:", job_descriptions)

    if st.button("Analyze Resumes"):
        analyze_and_store_resumes(selected_job)
        st.success("✅ Resume analysis completed.")

    resumes = get_analyzed_resumes()
    
    if not resumes:
        st.warning("⚠ No analyzed resumes found.")
    else:
        st.write("### Resume Analysis Results (Sorted by Score)")
        st.table([(candidate, score) for candidate, score, _ in resumes])  # Only display name & score

# ✅ Main UI (HR Option Selection)
def show_hr_ui():
    st.sidebar.title("HR Dashboard")
    page = st.sidebar.radio("Select an Option:", ["Job Role Specification", "HR Dashboard Analysis"])

    if page == "Job Role Specification":
        show_job_role_specification()
    else:
        show_hr_dashboard_analysis()