import mysql.connector
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"), 
        database=os.getenv("DB_NAME", "resume_db")   
    )

# Create main table
def create_main_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyzed_reports (
            report_id INT AUTO_INCREMENT PRIMARY KEY,
            job_id VARCHAR(50),
            user_id VARCHAR(50),
            analysis_report TEXT,
            tuned_resume TEXT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Table ensured to exist!")

# Flatten lists/dicts to JSON string
def flatten_value(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)

# Insert report into table
def store_report(analysis_report: dict, tuned_resume: dict, job_id=None, user_id=None):
    # Generate unique IDs if not provided
    timestamp = int(time.time())
    if user_id is None:
        user_id = f"USER_{timestamp}"
    if job_id is None:
        job_id = f"JOB_{timestamp}"
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convert dicts to JSON strings for storage
    analysis_str = flatten_value(analysis_report)
    tuned_str = flatten_value(tuned_resume)

    cursor.execute("""
        INSERT INTO reports (job_id, user_id, analysis_report, tuned_resume)
        VALUES (%s, %s, %s, %s)
    """, (job_id, user_id, analysis_str, tuned_str))

    conn.commit()
    cursor.close()
    conn.close()

    print("Row inserted successfully!")
    return job_id, user_id


# from google.colab import files
# print("Upload Resume PDF")
# resume_file = files.upload()
 
# print("Upload Job Description PDF")
# jd_file = files.upload()
