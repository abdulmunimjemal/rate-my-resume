from app.models.resume import ScoreResponse
import json 

# font result formatter

def format_fonts(fonts: dict) -> str:
    formatted_fonts = []
    for font, count in fonts.items():
        if font[0]:
            formatted_fonts.append(f"Font {font[0]} of Size {round(font[1])} pt appears {count} times\n")
        
    return "".join(formatted_fonts)

def parse_llm_response(response: str) -> ScoreResponse:
    try:
        result = response.replace('```', '')
        print(result)
        result = json.loads(result)
        return ScoreResponse(**result)
    except Exception as e:
        print(e)
        raise ValueError(f"Failed to parse LLM response: {e}")

