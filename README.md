# Rate My Resume: Resume Scoring API

This project provides a scalable FastAPI backend for scoring resumes using the TogetherLLM model. The API analyzes the content and format of resumes and provides a detailed score and feedback.

## Table of Contents

- [Rate My Resume: Resume Scoring API](#rate-my-resume-resume-scoring-api)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Score Resume](#score-resume)
    - [Health Checker](#health-checking)
  - [Project Structure](#project-structure)
  - [Contributing](#conributing)

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
- **Response**: `{'result_id': id }`

- **Endpoint**: `/resume/score/{id}`
- **Method**: `GET`
- **Request Body**: Result ID 
- **Response**: Feedback Details (Example Below)

- **Example Response** (for `GET /resume/score/{id}`):

  ```bash
  {
  "score": 83,
  "feedback": {
      "content": {
      "score": 80,
      "strengths": [
          "The resume contains all the necessary sections, including Experience, Relevant Projects, Education, and Contact information.",
          "The Skills section is well-organized and includes relevant programming languages, frameworks, and tools.",
          "The Experience section effectively describes impact and achievements, rather than just responsibilities."
      ],
      "areas_for_improvement": [
          "The resume includes a Relevant Courses section, which could be removed or greatly reduced.",
          "Some bullet points in the Experience section are a bit lengthy and could be broken up for better readability."
      ],
      "suggestions_for_enhancement": [
          "Consider adding more specific metrics or recognition to the Experience section to further demonstrate impact.",
          "Use bolding consistently throughout the resume to highlight achievements and technologies."
      ]
      },
      "format": {
      "score": 88,
      "strengths": [
          "The resume is well-organized and easy to read, with clear headings and bullet points.",
          "The use of whitespace is balanced, making the resume visually appealing."
      ],
      "areas_for_improvement": [
          "The font size is too small in some areas (7.5 pt), which may make it difficult to read.",
          "Some links are not clickable, which could make it harder for recruiters to access the candidate's online profiles."
      ],
      "suggestions_for_enhancement": [
          "Increase the font size to at least 10 pt to improve readability.",
          "Make sure all links are clickable to facilitate easy access to the candidate's online profiles."
      ]
      },
      "additionals": {
      "score": 77,
      "strengths": [
          "The resume effectively highlights achievements and recognition in the Experience section.",
          "The use of bolding to highlight technologies and tools is effective."
      ],
      "areas_for_improvement": [
          "Some sections, such as the Skills section, could be reorganized to better cater to the role."
      ],
      "suggestions_for_enhancement": [
          "Consider reorganizing the Skills section to prioritize the most relevant technologies and tools for the role.",
          "Use bolding more consistently throughout the resume to highlight achievements and technologies."
      ]
    }
  }
  ```
### Health Checking

- **Endpoint**: `/health/status/`
- **Method**: `GET`
- **Response**: JSON Response on Health Status of its Components

## Project Structure

The project structure is as follows:

```bash
rate-my-resume/
├── app/
│   ├── main.py
│   ├── config/
│   │   ├── config.py
│   │   ├── logging_config.py
│   ├── enums/
│   │   ├── file_extension.py
│   ├── models/
│   │   ├── resume.py
│   ├── routers/
│   │   ├── resume_router.py
│   │   ├── health_router.py
│   ├── services/
│   │   ├── resume_scoring.py
│   │   ├── file_parser.py
│   ├── utils/
│   │   ├── file_utils.py
│   │   ├── hashing_utils.py
│   │   ├── logger.py
│   │   ├── scoring_utils.py
├── .env
├── requirements.txt
└── README.md
```

## Conributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have any improvements or suggestions.
