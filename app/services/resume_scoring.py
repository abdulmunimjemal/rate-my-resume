from string import Template
from llama_index.llms.together import TogetherLLM
from app.config import settings
from app.models.resume import Resume, ScoreResponse
import json

llm = TogetherLLM(
    model=settings.MODEL_NAME,
    api_key=settings.TOGETHER_API_KEY,
    max_tokens=settings.MAX_TOKENS,
)

PROMPT_TEMPLATE = Template("""
    You are a resume review expert. Your task is to score the following resume based on the provided checklist, and then give detailed feedback with specific examples from the resume. The feedback should highlight areas of strength, areas for improvement, and include suggestions for enhancement.

    **Content Checklist (0-3 points each):**
    1. Contains the key sections/information: Experience, Relevant Projects, Education, and Contact information
    2. A Skills section is optional depending on the role. General roles likely don't need one, specific roles (e.g. React Developer) probably do.
    3. No soft skills in the Skills section. They say nothing: anyone can claim to be good at “communication” or “critical thinking”. You should demonstrate these skills through your bullet points in your experience section.
    4. No Summary of Qualifications. Your whole resume should be the summary!
    5. Experience includes your title, company, dates worked, and (optionally) location
    6. For contact information, include your email and (optionally) links to your personal website, GitHub account, and LinkedIn
    7. Unless the role asks for it, you don't need to include your physical address
    8. Resume is catered to the role. This can be as simple as re-ordering/selecting relevant skills and projects.
    9. Bullet points describe impact not just responsibilities (i.e. what was the result of your work, not just what your work was). The reader should also understand why your work was important to the company/project.

    **Format Checklist (0-3 points each):**
    1. Resume is one page max.
    2. For a one column resume, each bullet should be 2 lines max (3 lines max for a two column resume)
    3. No text has font size smaller than 10.
    4. Resume should be accessible and clear, even when printed in greyscale (no dark backgrounds, light text on light backgrounds, complex color patterns, etc).
    5. All links you have are clickable and not just plaintext.
    6. Bolded technologies/tools in your bullet points. This makes it easier for recruiters to see that you've actually used the tools/tech you claim to in your Skills section.
    7. Ensure capitalization is consistent throughout your resume, especially for the names of tools/technologies.
    8. All dates and date ranges use a consistent format (e.g. mmm yyyy - mmm yyyy as in May 2020 - Aug 2020).
    9. No acronyms unless they are listed in the job description (or are very common).
    10. Whitespace is balanced. If one section (e.g. skills, awards) is a bullet point list on the left side, consider making it a flat comma separated list or use two columns for just that section for visual balance.

    **Additionals Checklist (0-2 points each):**
    1. Bold achievements/recognition/metrics in your experience/projects. This is optional because you may have too much bold when combined with bolded tech/tools, so be wary of that.
    2. If you have relevant experience/projects, put that above your education (but this depends on the role!).
    3. Remove or greatly reduce your Relevant Courses section.
    4. Use between 1-4 bullet points per experience/project.

    Here is the resume:

    Number of Pages: 
        $pages
    Fonts: 
        $fonts
    Resume Text:
        $resume_text

    Score the resume based on the checklist and provide detailed feedback, including specific examples from the resume for improvement. Calculate the total score out of a possible 100 points.
    Return your whole response in JSON format, the response should start and end with the JSON with no additional texts from your side.
    It should have the following keys:
    - "score": the total score out of 100
    - "feedback": the detailed feedback with specific examples from the resume, including areas of strength, areas for improvement, and suggestions for enhancement

    USE THE FOLLOWING FORMAT FOR YOUR RESPONSE:
    ```
    {
        "score": 90,
        "feedback": {
            "content": {
                "strengths": [],
                "areas_for_improvement": [],
                "suggestions": []
            },
            "format": {
                "strengths": [],
                "areas_for_improvement": [],
                "suggestions": []
                },
            "additionals": {
                "strengths": [],
                "areas_for_improvement": [],
                "suggestions": []
            }
            
        }
    }```
    """)

def parse_llm_response(response: str) -> ScoreResponse:
    try:
        result = response.replace('```', '')
        print(result)
        result = json.loads(result)
        return ScoreResponse(**result)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {e}")


def score_resume(resume: Resume) -> ScoreResponse:
    prompt = PROMPT_TEMPLATE.substitute(
        pages=resume.pages,
        fonts=resume.fonts,
        resume_text=resume.text,
    )
    response = llm.stream_complete(prompt)
    result = []
    for chunk in response:
        result.append(chunk.delta)
    result = "".join(result)
    jsonified = parse_llm_response(result)
    return jsonified