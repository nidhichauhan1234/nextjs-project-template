from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from models.pdf_processor import PDFProcessor
from models.summarizer import DocumentSummarizer
from models.qa_engine import QAEngine

app = FastAPI(
    title="PDF Assistant API",
    description="Offline PDF processing with AI-powered summarization and Q&A",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
pdf_processor = PDFProcessor()
summarizer = DocumentSummarizer()
qa_engine = QAEngine()

class PDFUploadRequest(BaseModel):
    filename: str
    text: str
    pages: int
    size: int

class QAResponse(BaseModel):
    answer: str
    confidence: float
    references: List[dict]

class PDFData(BaseModel):
    id: str
    filename: str
    text: str
    headings: List[dict]
    summary: str
    pages: int
    size: int
    uploadDate: str

@app.get("/")
async def root():
    return {"message": "PDF Assistant API is running"}

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Process PDF
        result = pdf_processor.process_pdf(file.file, file.filename)
        
        return {
            "id": result["id"],
            "filename": result["filename"],
            "text": result["text"],
            "headings": result["headings"],
            "summary": result["summary"],
            "pages": result["pages"],
            "size": result["size"],
            "uploadDate": result["upload_date"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize")
async def summarize_document(request: dict):
    try:
        summary = summarizer.summarize(request["text"], request["headings"])
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/qa")
async def question_answer(request: dict):
    try:
        response = qa_engine.answer_question(
            request["question"],
            request["context"],
            request["headings"]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
