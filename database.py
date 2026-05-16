from models import Incident
from typing import List

incidents: List[Incident] = []
next_id: int = 1

def add_incident(incident: Incident) -> Incident:
    global next_id
    incident = incident.model_copy(update={"id": next_id})
    incidents.append(incident)
    next_id += 1
    return incident

def get_all_incidents() -> List[Incident]:
    return incidents

def get_incident_by_id(incident_id: int):
    matches = [i for i in incidents if i.id == incident_id]
    return matches[0] if matches else None

def update_incident_status(incident_id: int, new_status: str):
    for index, incident in enumerate(incidents):
        if incident.id == incident_id:
            incidents[index] = incident.model_copy(update={"status": new_status})
            return incidents[index]
    return None
