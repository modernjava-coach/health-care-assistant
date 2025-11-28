from fastapi import HTTPException, Query, APIRouter
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
    
    Args:
        request: SOAPNoteRequest containing the text and optional metadata
        provider: AI provider to use (aws or google)
    
    Returns:
        SOAPNoteResponse with the generated SOAP note
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

@router.post("/generate-codes", response_model=MedicalCodeResponse)
async def generate_medical_codes(
    request: MedicalCodeRequest, 
    provider: str = Query("aws", description="Provider to use: 'aws' or 'google'")
):
    """
    Extract medical codes (ICD-10 and CPT) from clinical text.
    
    Args:
        request: MedicalCodeRequest containing the text and options
        provider: AI provider to use (aws or google)
    
    Returns:
        MedicalCodeResponse with ICD-10 and CPT codes
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
