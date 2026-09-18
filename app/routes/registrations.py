from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from app.database import get_all_registrations, get_registration_by_id, update_decision_override, get_supabase_client
import json

router = APIRouter(tags=["Registrations & Events"])

class OverrideRequest(BaseModel):
    decision: str # approved | rejected
    reason: str

class EventCreateRequest(BaseModel):
    id: str
    name: str
    min_age: int = 18
    max_age: Optional[int] = None
    student_only: bool = False
    allowed_id_types: List[str] = ["aadhaar", "pan", "college_id", "voter_id"]

@router.get("/registrations")
def list_registrations(
    event_id: Optional[str] = Query(None, description="Filter by event ID"),
    status: Optional[str] = Query(None, description="Filter: approved | manual_review | rejected")
):
    results = get_all_registrations(event_id=event_id, status=status)
    return {
        "total": len(results),
        "registrations": results
    }

@router.get("/registrations/{reg_id}")
def get_registration(reg_id: str):
    record = get_registration_by_id(reg_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Registration {reg_id} not found")
    return record

@router.post("/registrations/{reg_id}/override")
def override_registration_decision(reg_id: str, body: OverrideRequest):
    record = get_registration_by_id(reg_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Registration {reg_id} not found")
    if body.decision not in ["approved", "rejected"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Decision override must be 'approved' or 'rejected'")

    update_decision_override(reg_id, body.decision, f"Organizer Override: {body.reason}")
    return {"status": "success", "registration_id": reg_id, "new_decision": body.decision}

@router.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreateRequest):
    client = get_supabase_client()
    client.table("events").upsert({
        "id": event.id,
        "name": event.name,
        "min_age": event.min_age,
        "max_age": event.max_age,
        "student_only": event.student_only,
        "allowed_id_types": event.allowed_id_types
    }).execute()
    return {"status": "created", "event_id": event.id}
