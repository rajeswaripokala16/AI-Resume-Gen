from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types
import fitz  # PyMuPDF
import os

# Load .env and get API key
load_dotenv()
api_key = os.getenv("AIzaSyC04ydcZXug2stn14TRNsxfx8BwRD2_WOU")

if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment. Check your .env file.")

# Configure Gemini client
client = genai.Client(api_key=api_key)

app = FastAPI(title="AI Resume Analyser")

# (Optional) CORS if you later call from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file given as bytes."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {e}")

def analyze_resume_with_gemini(resume_text: str) -> str:
    """Call Gemini to analyze the resume text and return feedback."""
    prompt = f"""
You are an expert resume reviewer for software engineering / tech roles.

Here is the resume content:

\"\"\"{resume_text}\"\"\"

1. Give a brief summary of this candidate.
2. List key strengths in bullet points.
3. List specific, actionable improvement suggestions in bullet points.
Keep the answer concise and clearly formatted.
"""
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.6,
                max_output_tokens=800,
            ),
        )
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    resume_text = extract_text_from_pdf(file_bytes)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    analysis = analyze_resume_with_gemini(resume_text)

    return {
        "success": True,
        "file_name": file.filename,
        "analysis": analysis,
    }
