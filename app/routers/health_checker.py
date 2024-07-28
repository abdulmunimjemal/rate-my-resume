from fastapi import APIRouter, HTTPException, Depends
from fastapi.routing import APIRoute
from app.config.config import settings
from llama_index.llms.together import TogetherLLM
import redis


router = APIRouter()

def get_redis_client():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD
    )

def get_llm_client():
    return TogetherLLM(
        model=settings.MODEL_NAME,
        api_key=settings.TOGETHER_API_KEY,
        max_tokens=settings.MAX_TOKENS,
    )

def check_llm_health(llm_client: TogetherLLM):
    try:
        llm_client.generate_response("Hello, world!")
        return True
    except Exception as e:
        return False

@router.get("/status", summary="API Health Check")
async def health_check(
    redis_client: redis.Redis = Depends(get_redis_client),
    llm_client: TogetherLLM = Depends(get_llm_client),
    routes: list[APIRoute] = Depends(lambda : router.routes)
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
    
    # Check if all routes are up
    for route in routes:
        try:
            response = await route.endpoint()
            if response.status_code == 500:
                raise Exception(f"Route {route.path} is down. HTTP Status Code: {response.status_code}")
        except Exception as e:
            health_status["details"][route.path] = str(e)
            health_status["status"] = "unhealthy"
    
    return health_status