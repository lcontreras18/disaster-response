from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import database
from models import IncidentReport, Incident
from ai_classifier import safe_classify

app = FastAPI(
    title="Emergency Disaster Response API",
    description="AI-powered emergency incident tracking system",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/health")
def health_check():
    return {"status": "online", "message": "Disaster Response API is running"}

@app.post("/incidents")
def create_incident(report: IncidentReport):
    ai_result = safe_classify(report.location, report.description)

    incident = Incident(
        id=0,
        location=report.location,
        description=report.description,
        reporter_name=report.reporter_name,
        severity=ai_result["severity"],
        category=ai_result["category"],
        summary=ai_result["summary"],
        timestamp=datetime.now(),
        status="ACTIVE"
    )

    saved = database.add_incident(incident)
    return saved

@app.get("/incidents")
def list_incidents():
    all_incidents = database.get_all_incidents()
    return {
        "count": len(all_incidents),
        "incidents": all_incidents
    }

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    incident = database.get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return incident

@app.patch("/incidents/{incident_id}/status")
def update_status(incident_id: int, status: str):
    valid_statuses = ["ACTIVE", "RESOLVED", "IN_PROGRESS"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    updated = database.update_incident_status(incident_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return updated

@app.get("/incidents/stats/summary")
def get_stats():
    all_incidents = database.get_all_incidents()
    severity_counts = {}
    category_counts = {}
    status_counts = {}

    for incident in all_incidents:
        s = incident.severity
        severity_counts[s] = severity_counts.get(s, 0) + 1

        c = incident.category
        category_counts[c] = category_counts.get(c, 0) + 1

        st = incident.status
        status_counts[st] = status_counts.get(st, 0) + 1

    return {
        "total": len(all_incidents),
        "by_severity": severity_counts,
        "by_category": category_counts,
        "by_status": status_counts
    }
