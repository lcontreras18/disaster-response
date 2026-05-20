# AI Powered Disaster Response

## Description

An AI-powered emergency incident tracking system. Users submit incident reports with a location and description, and the system uses Claude to automatically classify each report by severity (LOW, MEDIUM, HIGH, CRITICAL) and category (FLOOD, FIRE, MEDICAL, STRUCTURAL, OTHER). Reports are stored and exposed through a REST API with a simple HTML frontend.

## Key Features

- AI incident classification: each submitted report is automatically analyzed by Claude and assigned a severity level (LOW, MEDIUM, HIGH, CRITICAL), a category (FLOOD, FIRE, MEDICAL, STRUCTURAL, OTHER), and a one-sentence summary.
- Incident lifecycle tracking: incidents can be moved through three statuses (ACTIVE, IN_PROGRESS, RESOLVED) via the API.
- Stats endpoint: a summary endpoint breaks down all incidents by severity, category, and current status in a single request.
- Graceful fallback: if the AI classifier fails for any reason, the system defaults to MEDIUM severity and OTHER category rather than dropping the report.

## Tech Stack

- Python, FastAPI, Pydantic
- Anthropic Claude (claude-opus-4-5) for incident classification
- HTML/CSS frontend served as static files
- Docker for containerization

## Getting Started

### Prerequisites

- Python 3.10+
- An Anthropic API key

### Setup
  - Clone the repository:
    - git clone https://github.com/lcontreras18/disaster-response.git
    - cd disaster-response

  - Install dependencies:
    - pip install -r requirements.txt

  - Create a .env file in the project root and add your API key:
    - ANTHROPIC_API_KEY=your_api_key_here
    - Start the server:
    - uvicorn main:app --reload
    - The app will be available at http://localhost:8000.

  -  Running with Docker:
    - docker build -t disaster-response .
    - docker run -p 8000:8000 --env-file .env disaster-response

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serves the frontend |
| GET | `/health` | Health check |
| POST | `/incidents` | Submit a new incident report |
| GET | `/incidents` | List all incidents |
| GET | `/incidents/{id}` | Get a single incident |
| PATCH | `/incidents/{id}/status` | Update incident status (ACTIVE, IN_PROGRESS, RESOLVED) |
| GET | `/incidents/stats/summary` | Breakdown by severity, category, and status |

## Example Request

```json
POST /incidents
{
  "location": "Main St and 5th Ave",
  "description": "Large fire visible from the street, spreading to nearby buildings",
  "reporter_name": "Jane Doe"
}
```


  
