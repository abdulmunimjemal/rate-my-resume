from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resume_router, health_checker

app = FastAPI(
    title="Resume Scoring API",
    description="An AI-Based API to score resumes based on content and format.",
    version="1.0.0",
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router.router, prefix="/resume", tags=["resume"])
app.include_router(health_checker.router, prefix="/health", tags=["health"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Scoring API!"}