from fastapi import HTTPException, Query, APIRouter, UploadFile, File, Form
from typing import Optional
from ..services.llm_service import LLMService
from ..models import (
    SOAPNoteRequest,
    SOAPNoteResponse,
    MedicalCodeRequest,
    MedicalCodeResponse
)

# Initialize service
llm_service = LLMService()

# API Router
router = APIRouter()

@router.post("/generate-soap", response_model=SOAPNoteResponse)
async def generate_soap_note(
    request: SOAPNoteRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    """
    Generate a SOAP note from raw patient notes or transcripts.
    """
    try:
        soap_note = llm_service.generate_soap_note(
            text=request.text,
            provider_name=provider,
            patient_id=request.patient_id,
            provider_id=request.provider_id
        )
        
        return SOAPNoteResponse(
            soap_note=soap_note,
            provider=provider
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-soap-upload", response_model=SOAPNoteResponse)
async def generate_soap_note_upload(
    file: UploadFile = File(...),
    patient_id: Optional[str] = Form(None),
    provider_id: Optional[str] = Form(None),
    provider: str = Query("aws", description="Provider to use")
):
    """
    Generate a SOAP note from an uploaded file (Image or PDF).
    """
    try:
        content = await file.read()
        soap_note = llm_service.generate_soap_note_from_file(
            file_content=content,
            content_type=file.content_type,
            patient_id=patient_id,
            provider_id=provider_id
        )
        
        return SOAPNoteResponse(
            soap_note=soap_note,
            provider=provider
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-codes", response_model=MedicalCodeResponse)
async def generate_medical_codes(
    request: MedicalCodeRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    """
    Extract medical codes (ICD-10 and CPT) from clinical text.
    """
    try:
        codes_response = llm_service.generate_medical_codes(
            text=request.text,
            provider_name=provider,
            patient_id=request.patient_id,
            encounter_id=request.encounter_id
        )
        
        return codes_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-codes-upload", response_model=MedicalCodeResponse)
async def generate_medical_codes_upload(
    file: UploadFile = File(...),
    patient_id: Optional[str] = Form(None),
    encounter_id: Optional[str] = Form(None),
    provider: str = Query("aws", description="Provider to use")
):
    """
    Extract medical codes from an uploaded file (Image or PDF).
    """
    try:
        content = await file.read()
        codes_response = llm_service.generate_medical_codes_from_file(
            file_content=content,
            content_type=file.content_type,
            patient_id=patient_id,
            encounter_id=encounter_id
        )
        
        return codes_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

