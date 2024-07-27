from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.resume import Resume, ScoreResponse
from app.services.resume_scoring import score_resume
from app.services.file_parser import TextExtractor
from app.enums.file_extension import FileExtension
import json
import os

router = APIRouter()

@router.post("/score", response_model=ScoreResponse)
async def score_resume_endpoint(file: UploadFile = File(...)):
    try:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in {ext.value for ext in FileExtension}:
            raise HTTPException(status_code=400, detail="Invalid file type. Only .pdf and .docx files are supported.")
        # extraction 
        text_extractor = TextExtractor()
        file_path = f"tmp/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        try:
            text, pages, fonts = text_extractor.extract_text(file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error extracting text from the resume.")
        
        resume = Resume(text=text, pages=pages, fonts=fonts)
        result = score_resume(resume)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)