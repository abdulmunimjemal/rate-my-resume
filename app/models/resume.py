from pydantic import BaseModel

class Resume(BaseModel):
    text: str
    pages: int
    fonts: str

class ScoreResponse(BaseModel):
    score: int
    feedback: dict