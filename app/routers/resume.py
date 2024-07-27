from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.resume import Resume, ScoreResponse
from app.services.resume_scoring import score_resume
from app.services.file_parser import TextExtractor
from app.enums.file_extension import AllowedFileExtension
import json
import os

router = APIRouter()

@router.post("/score", response_model=ScoreResponse)
async def score_resume_endpoint(file: UploadFile = File(...)):
    file_path = f"tmp/{file.filename}"
    try:
        # Ensure the tmp directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in {ext.value for ext in AllowedFileExtension}:
            raise HTTPException(status_code=400, detail="Invalid file type. Only .pdf and .docx files are supported.")
        # extraction 
        text_extractor = TextExtractor()
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        try:
            text, pages, fonts = text_extractor.extract_text(file_path)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"Error extracting text from the resume.")
        
        resume = Resume(text=text, pages=pages, fonts=fonts)
        result = score_resume(resume)
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)