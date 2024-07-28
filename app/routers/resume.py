from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.models.resume import Resume, ScoreResponse
from app.services.resume_scoring import score_resume
from app.services.file_parser import TextExtractor
from app.enums.file_extension import AllowedFileExtension
from app.config.config import settings
from app.utils.file_utils import healthy_file_size
from app.utils.hashing_utils import calculate_file_hash
from llama_index.llms.together import TogetherLLM
import json, os
import redis

router = APIRouter()

# Dependency Injection for LLM client
def get_llm_client():
    return TogetherLLM(
    model=settings.MODEL_NAME,
    api_key=settings.TOGETHER_API_KEY,
    max_tokens=settings.MAX_TOKENS,
)

# Dependency Injection for Redis client
def get_redis_client():
    return redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD
)


@router.post("/score", response_model=dict)
async def score_resume_endpoint(
    file: UploadFile = File(...),
    redis_client: redis.Redis = Depends(get_redis_client),
    llm_client: TogetherLLM = Depends(get_llm_client)):
    file_path = f"tmp/{file.filename}"
    
    # file size check
    if not healthy_file_size(file.file):
        raise HTTPException(status_code=400, detail="File size is too large.")
    
    # file extension check
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in {ext.value for ext in AllowedFileExtension}:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .pdf and .docx files are supported.")
    
    # Check if result for this hash exists in Redis
    result_id = calculate_file_hash(file.file)
    cached_result = redis_client.get(result_id)
    if cached_result:
        print("Cached result found")
        return {"result_id": result_id } # the file hash as result id
    
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
        result = score_resume(resume, llm_client)
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