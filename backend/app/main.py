from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import os

app = FastAPI(title="AI Workflow Orchestrator - Backend")

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # react dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok"}

# simple upload endpoint (we will expand later)
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/ingest")
async def ingest_file(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return {"filename": file.filename, "path": path}
