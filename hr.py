import streamlit as st
import sqlite3

# ✅ Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_roles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_description TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# ✅ Save job description in SQLite
def save_job_description(description):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO job_roles (job_description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

# ✅ Function to show HR UI
def show_hr_ui():
    st.title("HR Dashboard")

    # ✅ Back button
    if st.button("🔙 Back to Home", use_container_width=True):
        st.session_state.selected_role = None
        st.rerun()

    # ✅ Selection buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Job Role Specification", use_container_width=True):
            st.session_state.hr_option = "job_specification"
            st.rerun()
    with col2:
        if st.button("📊 HR Dashboard Analysis", use_container_width=True):
            st.session_state.hr_option = "dashboard"
            st.rerun()

    # ✅ Display selected HR option
    if "hr_option" in st.session_state:
        if st.session_state.hr_option == "job_specification":
            show_job_role_specification()
        elif st.session_state.hr_option == "dashboard":
            show_hr_dashboard_analysis()

# ✅ Job Role Specification UI
def show_job_role_specification():
    st.subheader("Job Role Specification")
    job_description = st.text_area("Enter Job Description & Requirements", height=150)

    if st.button("💾 Save Job Description"):
        if job_description.strip():
            save_job_description(job_description)
            st.success("Job Description Saved Successfully!")
        else:
            st.error("Please enter a valid job description.")

# ✅ HR Dashboard Analysis (Dummy Data)
def show_hr_dashboard_analysis():
    st.subheader("HR Dashboard Analysis")

    # Dummy resume analysis data
    dummy_data = [
        {"Candidate Name": "John Doe", "Score": 85, "Skills Match": "High", "Experience": "5 years"},
        {"Candidate Name": "Jane Smith", "Score": 78, "Skills Match": "Medium", "Experience": "3 years"},
        {"Candidate Name": "Mike Johnson", "Score": 92, "Skills Match": "Very High", "Experience": "7 years"}
    ]

    st.table(dummy_data)

# ✅ Initialize database
init_db()
