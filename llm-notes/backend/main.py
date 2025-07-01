import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from summarizer import generate_summary_and_keywords
from file_reader import extract_text

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)

    if not text.strip():
        return JSONResponse({"error": "Could not extract any text from file."}, status_code=400)

    result = generate_summary_and_keywords(text)
    return result

@app.get("/")
def root():
    return {"message": "LLM Summarizer backend is running."}
