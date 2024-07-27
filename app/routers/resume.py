from fastapi import APIRouter, HTTPException, UploadFile, File
from llama_index.llms.together import TogetherLLM
from app.models.resume import Resume, ScoreResponse
from app.services.resume_scoring import score_resume
from app.services.file_parser import TextExtractor
from app.enums.file_extension import AllowedFileExtension
from app.config import settings
import json, os
import redis, uuid
from hashlib import sha256

router = APIRouter()

# Initialize the LLM
llm = TogetherLLM(
    model=settings.MODEL_NAME,
    api_key=settings.TOGETHER_API_KEY,
    max_tokens=settings.MAX_TOKENS,
)

# Set up Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD
)

# calculate file size, if it is greater than 10MB, return False, else return True
def healthy_file_size(file, max_size=2):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    return file_size <= max_size * 1024 * 1024
    

@router.post("/score", response_model=dict)
async def score_resume_endpoint(file: UploadFile = File(...)):
    file_path = f"tmp/{file.filename}"
    
    # file size check
    if not healthy_file_size(file.file):
        raise HTTPException(status_code=400, detail="File size is too large.")
    
    # file extension check
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in {ext.value for ext in AllowedFileExtension}:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .pdf and .docx files are supported.")
    
    # upload dir existance check
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    text_extractor = TextExtractor()
        
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    try:
        text, pages, fonts = text_extractor.extract_text(file_path)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error extracting text from the resume.")
    try:
        resume = Resume(text=text, pages=pages, fonts=fonts)
        result = score_resume(resume, llm)
        result_id = str(uuid.uuid4())
        redis_client.set(result_id, json.dumps(result.dict()), ex=settings.REDIS_EXPIRATION)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error scoring the resume.")
    
    # post processing cleanup
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"result_id": result_id}

@router.get("/score/{result_id}", response_model=ScoreResponse)
async def get_result(result_id: str):
    result = redis_client.get(result_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found.")
    return ScoreResponse(**json.loads(result))