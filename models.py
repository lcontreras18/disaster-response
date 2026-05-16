from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentReport(BaseModel):
    location: str
    description: str
    reporter_name: Optional[str] = "Anonymous"

class Incident(BaseModel):
    id: int
    location: str
    description: str
    reporter_name: str
    severity: str
    category: str
    summary: str
    timestamp: datetime
    status: str = "ACTIVE"
