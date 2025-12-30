# Import libraries
import PyPDF2
import google.generativeai as genai
import json

# Import DB helpers
from db import create_main_table, store_report

# Upload Resume & Job Description PDFs
resume_path = r"C:\Users\91891\prompting\RESUME - UPDATED (2).pdf"
jd_path = r"C:\Users\91891\prompting\Job Description.pdf"

# Extract text from PDFs
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

resume_text = extract_text_from_pdf(resume_path)
jd_text = extract_text_from_pdf(jd_path)

# Configure Gemini API
genai.configure(api_key="AIzaSyCx9fh8GnS3uKvmOGoXNKLIu0EZX-Z58p0")
model = genai.GenerativeModel("gemini-1.5-flash")

# ----- Analysis Prompt -----
prompt_analysed = {
    "task": "You are a resume analyzer. Generate an analysed report with scores by comparing resume and job description.",
    "inputs": {
        "resume": resume_text,
        "job_description": jd_text
    },
    "output_requirements": {
        "Summary_of_the_resume": "Provide a detailed summary of the candidate with max 8 points",
        "Education": "Summarize education details and domains",
        "Experience": "Highlight total years of experience and match with job description",
        "Recent_Industry_Experience": "Evaluate how relevant the candidate's industry experience matches the job description and assign a score(0-100)",
        "Strengths_and_Weakness": "Identify candidate's strengths and weaknesses aligned with JD and assign a balance score(0-100)",
        "Employment_Stability": "Assess employment stability and assign score(0-100)",
        "Roles_and_Responsibility_Match": "Compare roles and responsibilities with JD and assign score(0-100)",
        "Final_Score": "Provide a final score out of 100",
        "Hire_Recommendation": "Provide recommendation based on final score"
    }
}

# ----- Tuned Resume Prompt -----
prompt_tuned = {
    "task": "You are a resume tuner. Rewrite the resume so it aligns with the job description.",
    "inputs": {
        "resume": resume_text,
        "job_description": jd_text
    },
    "rules": {
        "fabrication": "Do NOT fabricate new skills, degrees, experience, or job titles",
        "style": "Keep resume concise, ATS-friendly, and professional",
        "format": "Use bullet points wherever possible"
    }
}

# Convert prompts to JSON text
prompt_analysed_text = json.dumps(prompt_analysed, indent=2)
prompt_tuned_text = json.dumps(prompt_tuned, indent=2)

# Generate analysis report
response_analysis = model.generate_content(prompt_analysed_text)
analysis_report = response_analysis.text
print("Analysis Report Generated!")
print(analysis_report)

# Generate tuned resume
response_tuned = model.generate_content(prompt_tuned_text)
tuned_resume = response_tuned.text
print("Tuned Resume Generated!")
print(tuned_resume)

# Ensure MySQL table exists
create_main_table()

analysis_report_json = {"Full Report":analysis_report}

tuned_resume_json = {"Full Report": tuned_resume}

# Store both analysis and tuned resume in MySQL
job_id, user_id = store_report(analysis_report_json, tuned_resume_json)
print(f"Analysis and tuned resume stored for: {user_id} with Job ID: {job_id}")