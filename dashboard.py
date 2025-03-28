import streamlit as st
from resumeAnalysis import analyze_and_store_resumes, get_analyzed_resumes, get_job_descriptions

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
    
    filtered_resumes = [(candidate, score) for candidate, score, job in resumes if job == selected_job]
    
    if not filtered_resumes:
        st.warning("⚠ No analyzed resumes found for this job description.")
    else:
        st.write(f"### Resume Analysis Results for '{selected_job}' (Sorted by Score)")
        st.table(filtered_resumes)  # Display only candidate name and score