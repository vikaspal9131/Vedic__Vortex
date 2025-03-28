import os
import pdfplumber
import sqlite3
import dotenv
import json
from google import genai

dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai_client = genai.Client(api_key=API_KEY)
DB_PATH = "resumes.db"

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resume_analysis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        candidate_name TEXT,
                        score INTEGER,
                        tech_stacks TEXT,
                        summary TEXT,
                        file_path TEXT,
                        job_description TEXT)''')
    conn.commit()
    conn.close()

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n" if page.extract_text() else ""
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text.strip()

def process_gemini_output(output):
    try:
        output = output.replace("```json", "").replace("```python", "").replace("```", "").strip()
        return json.loads(output)
    except Exception as e:
        print(f"Error processing Gemini output: {e}")
        return {"score": 0, "summary": "", "tech_stacks": []}

def get_resume_analysis(resume_text, job_description):
    if not resume_text:
        return {"score": 0, "summary": "", "tech_stacks": []}
    
    prompt = (
        f"Analyze this resume based on the following job description:\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Resume:\n{resume_text}\n\n"
        "Provide the output in JSON format with the following keys:\n"
        "- 'score': An integer out of 100.\n"
        "- 'summary': A short summary of the candidate's experience and skills.\n"
        "- 'tech_stacks': A list of technologies the candidate has experience with."
    )
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        response_text = response.candidates[0].content.parts[0].text  
        return process_gemini_output(response_text)
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return {"score": 0, "summary": "", "tech_stacks": []}

def analyze_and_store_resumes(job_description):
    initialize_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resume_analysis WHERE job_description = ?", (job_description,))
    resume_folder = "resume"
    resumes = [f for f in os.listdir(resume_folder) if f.endswith(".pdf")]
    for resume in resumes:
        pdf_path = os.path.join(resume_folder, resume)
        resume_text = extract_text_from_pdf(pdf_path)
        analysis = get_resume_analysis(resume_text, job_description)
        candidate_name = resume.replace(".pdf", "").replace("_", " ").title()
        cursor.execute("""
            INSERT INTO resume_analysis (candidate_name, score, tech_stacks, summary, file_path, job_description)
            VALUES (?, ?, ?, ?, ?, ?)""", 
            (candidate_name, analysis["score"], json.dumps(analysis["tech_stacks"]), analysis["summary"], pdf_path, job_description))
    conn.commit()
    conn.close()

def get_analyzed_resumes():
    initialize_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT candidate_name, score, tech_stacks, summary, job_description FROM resume_analysis ORDER BY score DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def get_job_descriptions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM job_descriptions")
    jobs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jobs
