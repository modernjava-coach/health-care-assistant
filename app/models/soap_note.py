from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SOAPNoteType(str, Enum):
    """Types of SOAP notes"""
    INITIAL_CONSULTATION = "initial_consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    ROUTINE_CHECKUP = "routine_checkup"


class SOAPNote(BaseModel):
    """Domain model for SOAP (Subjective, Objective, Assessment, Plan) notes"""
    
    id: Optional[str] = Field(None, description="Unique identifier for the SOAP note")
    patient_id: Optional[str] = Field(None, description="Patient identifier")
    provider_id: Optional[str] = Field(None, description="Healthcare provider identifier")
    encounter_date: Optional[datetime] = Field(None, description="Date and time of the encounter")
    note_type: Optional[SOAPNoteType] = Field(None, description="Type of SOAP note")
    
    # SOAP Components
    subjective: str = Field(..., description="Subjective: Patient's description of symptoms and concerns")
    objective: str = Field(..., description="Objective: Observable and measurable findings")
    assessment: str = Field(..., description="Assessment: Diagnosis or clinical impression")
    plan: str = Field(..., description="Plan: Treatment plan and follow-up instructions")
    
    # Additional metadata
    chief_complaint: Optional[str] = Field(None, description="Primary reason for visit")
    vital_signs: Optional[dict] = Field(None, description="Vital signs measurements")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when note was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when note was last updated")
    
    # AI Generation metadata
    generated_by_ai: bool = Field(False, description="Whether this note was AI-generated")
    ai_provider: Optional[str] = Field(None, description="AI provider used (aws, google, etc.)")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI confidence score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "P12345",
                "provider_id": "DR001",
                "encounter_date": "2024-11-28T10:30:00Z",
                "note_type": "follow_up",
                "subjective": "Patient reports persistent headaches for the past week, occurring daily in the morning.",
                "objective": "BP: 120/80, HR: 72, Temp: 98.6°F. Patient appears alert and oriented.",
                "assessment": "Tension headaches, likely stress-related. No signs of neurological deficit.",
                "plan": "Prescribe ibuprofen 400mg PRN. Recommend stress management techniques. Follow-up in 2 weeks if symptoms persist.",
                "chief_complaint": "Headaches",
                "generated_by_ai": True,
                "ai_provider": "aws"
            }
        }


class SOAPNoteRequest(BaseModel):
    """Request model for generating SOAP notes"""
    text: str = Field(..., description="Input text/transcript to generate SOAP note from")
    patient_id: Optional[str] = Field(None, description="Optional patient identifier")
    provider_id: Optional[str] = Field(None, description="Optional provider identifier")
    note_type: Optional[SOAPNoteType] = Field(None, description="Type of SOAP note")
    include_metadata: bool = Field(True, description="Whether to include additional metadata")


class SOAPNoteResponse(BaseModel):
    """Response model for SOAP note generation"""
    soap_note: SOAPNote = Field(..., description="Generated SOAP note")
    provider: str = Field(..., description="AI provider used for generation")
    processing_time_ms: Optional[float] = Field(None, description="Time taken to generate the note")
