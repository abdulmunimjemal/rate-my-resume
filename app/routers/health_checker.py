from fastapi import APIRouter, HTTPException, Depends
from fastapi.routing import APIRoute
from app.config.config import settings
from llama_index.llms.together import TogetherLLM
import redis

router = APIRouter()

# Dependency for Redis client
def get_redis_client():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD
    )

# Dependency for LLM client
def get_llm_client():
    return TogetherLLM(
        model=settings.MODEL_NAME,
        api_key=settings.TOGETHER_API_KEY,
        max_tokens=settings.MAX_TOKENS,
    )

# Health check function for LLM
def check_llm_health(llm_client: TogetherLLM):
    try:
        # imple check by generating a response
        llm_client.complete("Hello, World!")
        return True
    except Exception as e:
        return False

@router.get("/status", summary="API Health Check")
async def health_check(
    redis_client: redis.Redis = Depends(get_redis_client),
    llm_client: TogetherLLM = Depends(get_llm_client),
):
    health_status = {
        "status": "healthy",
        "details": {}
    }

    # Redis
    try:
        if not redis_client.ping():
            raise Exception("Redis is down. Can't Ping.")
        health_status["details"]["redis"] = "healthy"
    except Exception as e:
        health_status["details"]["redis"] = str(e)
        health_status["status"] = "unhealthy"

    # LLM
    try:
        if not check_llm_health(llm_client):
            raise Exception("LLM is down")
        health_status["details"]["llm"] = "healthy"
    except Exception as e:
        health_status["details"]["llm"] = str(e)
        health_status["status"] = "unhealthy"

    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=500, detail=health_status)

    return health_status
