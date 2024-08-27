from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List

class Resume(BaseModel):
    text: str
    pages: int
    fonts: str

class FeedbackDetails(BaseModel):
    score: int = Field(description="The score out of 100")
    strength: List[str] = Field(description="Areas of strength")
    areas_for_improvement: List[str] = Field(description="Areas for improvement")
    suggestions: List[str] = Field(description="Suggestions for enhancement")

class Feedback(BaseModel):
    content: FeedbackDetails = Field(description="Feedback on content")
    format: FeedbackDetails = Field(description="Feedback on format")
    additionals: FeedbackDetails = Field(description="Additional feedback")

class ScoreResponse(BaseModel):
    score: int = Field(description="The total score out of 100")
    feedback: Feedback = Field(description="Detailed feedback with specific examples from the resume")


