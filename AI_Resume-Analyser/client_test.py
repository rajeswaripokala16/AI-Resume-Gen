# client_test.py
import requests

API_URL = "http://127.0.0.1:8000/analyze"

def main():
    job_title = "Software Engineer Intern"
    seniority = "intern"
    job_description = """
Looking for a Software Engineering Intern who is currently a student (B.Tech/B.E),
with strong fundamentals in Data Structures & Algorithms and experience with
Python or Java plus basic web development (HTML, CSS, JS or React).
    """

    resume_text = """
I am a 3rd year B.Tech CSE student experienced with Java, Python, and
full‑stack projects using React and FastAPI. I have built portfolio projects
(vision-based systems, food donation platform), solved 300+ DSA problems, and
am actively learning system design and backend development.
    """

    payload = {
        "job_title": job_title,
        "seniority": seniority,
        "job_description": job_description,
        "resume_text": resume_text,
    }

    resp = requests.post(API_URL, json=payload)
    print("Status:", resp.status_code)
    print("Response JSON:")
    print(resp.json())

if __name__ == "__main__":
    main()
