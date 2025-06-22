
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from pdf_reader import extract_text_from_pdf
from summarizer import generate_summary_and_keywords

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    if not text:
        return JSONResponse({"error": "Failed to extract text."}, status_code=400)

    result = generate_summary_and_keywords(text)
    return result
