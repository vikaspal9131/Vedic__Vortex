import streamlit as st

def show_hr_ui():
    st.title("HR Dashboard")
    st.write("Welcome, HR! Manage resumes and shortlist candidates.")

    if st.button("🔙 Back to Home", use_container_width=True):
        st.session_state.selected_role = None  # ✅ Reset selection
        st.rerun()

    # Add HR-specific functionality here
    if st.button("View Resumes"):
        st.write("Showing analyzed resumes...")
