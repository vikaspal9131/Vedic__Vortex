import streamlit as st
import pandas as pd
from resumeAnalysis import analyze_and_store_resumes, get_analyzed_resumes, get_job_descriptions

def show_hr_dashboard_analysis():
    st.title("📊 HR Dashboard Analysis")

    # Initialize session state variables
    if "selected_resume" not in st.session_state:
        st.session_state.selected_resume = None
    if "min_score" not in st.session_state:
        st.session_state.min_score = 50  # Default minimum score

    job_descriptions = get_job_descriptions()

    if not job_descriptions:
        st.warning("⚠ No job descriptions found. Please add one first.")
        return

    selected_job = st.selectbox("Select a Job Description:", job_descriptions)

    if st.button("Analyze Resumes"):
        analyze_and_store_resumes(selected_job)
        st.success("✅ Resume analysis completed.")

    resumes = get_analyzed_resumes()

    # Extract only relevant resumes
    filtered_resumes = [
        (candidate, score, summary, tech_stacks) 
        for candidate, score, summary, tech_stacks, job in resumes if job == selected_job
    ]

    # Input field for minimum score using session state
    st.session_state.min_score = st.number_input(
        "Enter minimum score to shortlist candidates:",
        min_value=0, max_value=100, step=1, value=st.session_state.min_score
    )

    # Apply minimum score filtering from session state
    shortlisted_resumes = [res for res in filtered_resumes if res[1] >= st.session_state.min_score]

    if not shortlisted_resumes:
        st.warning("⚠ No candidates meet the minimum score requirement.")
    else:
        st.write(f"### Shortlisted Candidates for '{selected_job}'")

        # Create table structure
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write("**Candidate**")
        col2.write("**Score**")
        col3.write("**Details**")

        for candidate, score, summary, tech_stacks in shortlisted_resumes:
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(candidate)
            col2.write(score)
            if col3.button(f"🔍 View", key=candidate):
                st.session_state.selected_resume = (candidate, summary, tech_stacks)

        # Convert shortlisted resumes to DataFrame for CSV export
        df = pd.DataFrame(shortlisted_resumes, columns=["Candidate", "Score", "Summary", "Tech Stacks"])
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Shortlist",
            data=csv,
            file_name="shortlisted_candidates.csv",
            mime="text/csv"
        )

    # Sidebar for detailed view
    with st.sidebar:
        st.header("📜 Resume Details")
        if st.session_state.selected_resume:
            candidate, summary, tech_stacks = st.session_state.selected_resume
            st.subheader(f"**{candidate}**")
            st.markdown(f"**Summary:**\n{summary}")
            st.markdown(f"**Tech Stacks:**\n{tech_stacks}")
            if st.button("Close Details"):
                st.session_state.selected_resume = None
