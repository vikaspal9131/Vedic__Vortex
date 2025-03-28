import sqlite3
import streamlit as st

DB_PATH = "resumes.db"

def save_job_description(description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_descriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT)''')
    cursor.execute("INSERT INTO job_descriptions (description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

def show_job_role_specification():
    st.title("📝 Job Role Specification")
    job_description = st.text_area("Enter Job Description:", height=200)
    
    if st.button("Save Job Description"):
        if job_description.strip():
            save_job_description(job_description)
            st.success("✅ Job description saved successfully!")
        else:
            st.warning("⚠ Please enter a valid job description.")