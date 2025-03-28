import streamlit as st
from job_role import show_job_role_specification
from dashboard import show_hr_dashboard_analysis

def show_hr_ui():
    st.sidebar.title("HR Dashboard")
    page = st.sidebar.radio("Select an Option:", ["Job Role Specification", "HR Dashboard Analysis"])

    if page == "Job Role Specification":
        show_job_role_specification()
    else:
        show_hr_dashboard_analysis()