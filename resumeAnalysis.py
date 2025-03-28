import os
import pdfplumber
import sqlite3
import dotenv
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

def get_resume_score(resume_text, job_description):
    if not resume_text:
        return 0
    
    prompt = f"Evaluate this resume for the following job description:\n\n{job_description}\n\nResume:\n{resume_text}\n\nGive a score out of 100."
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        response_text = response.candidates[0].content.parts[0].text  
        score_line = response_text.split("\n")[2]  
        score = int(score_line.split(":")[1].strip().split("/")[0])  
        return max(0, min(100, score))
    except Exception as e:
        print(f"Error analyzing resume score: {e}")
        return 0  

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
        score = get_resume_score(resume_text, job_description)
        candidate_name = resume.replace(".pdf", "").replace("_", " ").title()
        cursor.execute("INSERT INTO resume_analysis (candidate_name, score, file_path, job_description) VALUES (?, ?, ?, ?)", 
                       (candidate_name, score, pdf_path, job_description))
    conn.commit()
    conn.close()

def get_analyzed_resumes():
    initialize_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT candidate_name, score, job_description FROM resume_analysis ORDER BY score DESC")
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