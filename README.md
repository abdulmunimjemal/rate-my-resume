# Rate My Resume: Resume Scoring API

This project provides a scalable FastAPI backend for scoring resumes using the TogetherLLM model. The API analyzes the content and format of resumes and provides a detailed score and feedback.

## Table of Contents

- [Rate My Resume: Resume Scoring API](#rate-my-resume-resume-scoring-api)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Score Resume](#score-resume)
  - [Conributing](#conributing)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/abdulmunimjemal/rate-my-resume.git
    cd rate-my-resume
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set the environment variables**:
   Create a `.env` file in the root directory and add the following environment variables: (check `.env.sample` for a sample)
   ```bash
   TOGETHER_API_KEY=your_together_api_key
   ```

## Usage

1. **Run the FastAPI server**:

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**:
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation provided by Swagger UI.

## API Endpoints

### Score Resume

- **Endpoint**: `/resume/score`
- **Method**: `POST`
- **Request Body**: Upload a file (`.pdf` or `.docx`)
- **Response**: Returns the score and feedback for the uploaded resume
- **Example**:

````json
{
 "score": 84,
 "feedback": "The resume is well-structured and effectively showcases the candidate's technical skills and experience. However, there are some areas that need improvement.\n\n**Content Checklist:**\nThe resume contains all the necessary sections, including Experience, Education, and Contact information. The Skills section is well-organized, but it includes language skills, which could be removed. The Experience section effectively demonstrates the candidate's technical skills and achievements.\n\n* Strength: The candidate's achievements and impact are clearly stated in the Experience section, such as 'achieving 80% better response time' and 'contributing to a 60% increase in quarterly revenue.'\n* Improvement: The Relevant Courses section is not necessary and could be removed. The candidate's education is already stated, and the courses listed do not add significant value.\n\n**Format Checklist:**\nThe resume is one page long, and the font size is mostly consistent. However, the font size of 7.5 pt is too small and should be increased to at least 10 pt.\n* Improvement: The font size of 7.5 pt should be increased to at least 10 pt. The links to the candidate's GitHub and LinkedIn profiles are not clickable and should be made clickable.\n\n**Additionals Checklist:**\nThe candidate's achievements are bolded, but not consistently throughout the resume. The Relevant Projects section is well-organized, but the dates could be formatted consistently.\n* Improvement: The dates in the Relevant Projects section should be formatted consistently, such as 'Feb 2021 - June 2022' instead of 'Feb 2021 – June 2022.'\n* Increase the font size of 7.5 pt to at least 10 pt.\n* Make the links to the candidate's GitHub and LinkedIn profiles clickable.\n* Format the dates in the Relevant Projects section consistently.\n* Consider adding a brief summary or overview of the candidate's experience and skills at the top of the resume.\n* Consider bolding the candidate's achievements consistently throughout the resume."
}```

## Project Structure
The project structure is as follows:

```bash
fastapi-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── enums/
│   │   ├── __init__.py
│   │   ├── file_extension.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── resume.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── resume.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── resume_scoring.py
│   │   ├── file_parser.py
├── .env
├── requirements.txt
└── README.md
````

## Conributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have any improvements or suggestions.
