import streamlit as st

def show_candidate_ui():
    st.title("Candidate Dashboard")
    st.write("Upload your resume and receive AI-based feedback.")

    if st.button("Back to Home"):
        st.query_params.clear()  # ✅ Clears query params to return to the home screen
        st.rerun()

    uploaded_file = st.file_uploader("Upload your resume (PDF/Docx)", type=["pdf", "docx"])
    
    if uploaded_file:
        st.success("Resume uploaded successfully!")
