import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TOGETHER_API_KEY: str = os.getenv("OPENAI_API_KEY") # get this from https://www.together.ai/
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini") # https://docs.together.ai/docs/inference-models
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 4096)) # max tokens to generate
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost") # redis host
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379)) # redis port
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "") # redis password 
    REDIS_EXPIRATION: int = int(os.getenv("REDIS_EXPIRATION", 3600)) # redis expiration time in seconds

settings = Settings()