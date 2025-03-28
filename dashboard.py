import streamlit as st
from resumeAnalysis import analyze_and_store_resumes, get_analyzed_resumes, get_job_descriptions

def show_hr_dashboard_analysis():
    st.title(" HR Dashboard Analysis")

    # Initialize session state for sidebar details
    if "selected_resume" not in st.session_state:
        st.session_state.selected_resume = None

    job_descriptions = get_job_descriptions()

    if not job_descriptions:
        st.warning("⚠ No job descriptions found. Please add one first.")
        return

    selected_job = st.selectbox("Select a Job Description:", job_descriptions)

    if st.button("Analyze Resumes"):
        analyze_and_store_resumes(selected_job)
        st.success("✅ Resume analysis completed.")

    resumes = get_analyzed_resumes()
    
    # Ensure correct unpacking
    filtered_resumes = [
        (candidate, score, summary, tech_stacks) 
        for candidate, score, summary, tech_stacks, job in resumes if job == selected_job
    ]

    # UPDATED: Added an input field for minimum score
    min_score = st.number_input(
        "Enter minimum score to shortlist candidates (leave blank to show all):",
        min_value=0, max_value=100, step=1, value=None
    )

    # UPDATED: Apply score-based filtering if a score is provided
    if min_score is not None:
        filtered_resumes = [res for res in filtered_resumes if res[1] >= min_score]

    if not filtered_resumes:
        st.warning("⚠ No analyzed resumes found for this job description.")
    else:
        st.write(f"### Resume Analysis Results for '{selected_job}' (Click on a row for details)")

        # Create table structure
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write("**Candidate**")
        col2.write("**Score**")
        col3.write("**Details**")

        for candidate, score, summary, tech_stacks in filtered_resumes:
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(candidate)
            col2.write(score)
            # Button to trigger sidebar update
            if col3.button(f"🔍 View", key=candidate):
                st.session_state.selected_resume = (candidate, summary, tech_stacks)

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
