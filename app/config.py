import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY") # get this from https://www.together.ai/
    MODEL_NAME: str = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo") # https://docs.together.ai/docs/inference-models
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 1024)) # max tokens to generate 

settings = Settings()