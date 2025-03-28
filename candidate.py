import streamlit as st
import os
import time
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Predefined job description
JOB_DESCRIPTION = "Responsible for developing scalable web applications using Python and JavaScript. Must have experience with cloud computing and AI technologies."

# Ensure 'resume' folder exists
RESUME_FOLDER = "resume"
os.makedirs(RESUME_FOLDER, exist_ok=True)

class ATSAnalyzer:
    @staticmethod
    def extract_text_from_pdf(file_path):
        try:
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
            return text
        except Exception as e:
            st.error(f"Error extracting PDF text: {str(e)}")
            return None

    @staticmethod
    def analyze_text_with_ai(text):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")  # Initialize Model
            response = model.generate_content(
                f"""
        As an ATS (Applicant Tracking System) expert, analyze this resume against the job description below:

        **Job Description:**  
        {JOB_DESCRIPTION}

        **Resume Text:**  
        {text}

        Provide the following insights:  
        1. **Overall match percentage (%)**  
        2. **Key matching keywords found**  
        3. **Important missing keywords**  
        4. **Skills gap analysis**  
        5. **Specific recommendations for improvement**  

        Start your response by prominently displaying the match percentage.
        """
            )
            return response.text if response else "Analysis could not be generated."
        except Exception as e:
            return f"Error in AI analysis: {str(e)}"

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the 'resume' folder."""
    file_path = os.path.join(RESUME_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save file content
    return file_path

def analyze_resume(file_path):
    st.info("Analyzing resume with AI...", icon="ℹ️")
    time.sleep(2)
    extracted_text = ATSAnalyzer.extract_text_from_pdf(file_path)
    if extracted_text:
        analysis_result = ATSAnalyzer.analyze_text_with_ai(extracted_text)
        st.success("Resume analysis complete!", icon="✅")
        return analysis_result
    else:
        st.error("Failed to analyze resume.", icon="❌")
        return None

def show_candidate_ui():
    st.sidebar.title("Candidate Portal")
    
    # Removed "HR Dashboard" from the options
    page = st.sidebar.radio("Select an Option:", ["Upload Resume", "View Analysis"])  # **Updated here**

    if page == "Upload Resume":
        st.subheader("Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF format)",
            type=["pdf"],
            help="Ensure your resume is in PDF format"
        )

        if uploaded_file:
            st.success("PDF uploaded successfully!")
            file_path = save_uploaded_file(uploaded_file)
            st.success(f"File saved at: {file_path}", icon="📂")
            
            if st.button("Analyze Resume"):
                analysis_result = analyze_resume(file_path)
                st.session_state.analysis_result = analysis_result  # Store result
                st.success("Resume analysis complete!")
    
    elif page == "View Analysis":
        st.subheader("ATS Analysis Result")
        if "analysis_result" in st.session_state and st.session_state.analysis_result:
            st.text_area("", st.session_state.analysis_result, height=400)
        else:
            st.info("No analysis found. Please upload and analyze your resume first.")

    # Removed "HR Dashboard" logic **Updated here**
    
    st.markdown("---")
