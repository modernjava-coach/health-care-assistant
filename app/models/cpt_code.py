from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CPTCategory(str, Enum):
    """CPT code categories"""
    EVALUATION_MANAGEMENT = "99201-99499"  # E&M codes
    ANESTHESIA = "00100-01999"
    SURGERY = "10021-69990"
    RADIOLOGY = "70010-79999"
    PATHOLOGY_LABORATORY = "80047-89398"
    MEDICINE = "90281-99607"


class CPTModifier(str, Enum):
    """Common CPT modifiers"""
    BILATERAL = "50"  # Bilateral procedure
    MULTIPLE_PROCEDURES = "51"  # Multiple procedures
    REDUCED_SERVICES = "52"  # Reduced services
    DISCONTINUED = "53"  # Discontinued procedure
    SURGICAL_CARE_ONLY = "54"  # Surgical care only
    POSTOPERATIVE_ONLY = "55"  # Postoperative management only
    PREOPERATIVE_ONLY = "56"  # Preoperative management only
    DECISION_FOR_SURGERY = "57"  # Decision for surgery
    STAGED_PROCEDURE = "58"  # Staged or related procedure
    DISTINCT_PROCEDURE = "59"  # Distinct procedural service
    TWO_SURGEONS = "62"  # Two surgeons
    ASSISTANT_SURGEON = "80"  # Assistant surgeon
    MINIMUM_ASSISTANT = "81"  # Minimum assistant surgeon
    ASSISTANT_RESIDENT = "82"  # Assistant surgeon (resident unavailable)
    REPEAT_PROCEDURE = "76"  # Repeat procedure by same physician
    REPEAT_DIFFERENT = "77"  # Repeat procedure by different physician
    UNPLANNED_RETURN = "78"  # Unplanned return to OR
    UNRELATED_PROCEDURE = "79"  # Unrelated procedure during postop period
    PROFESSIONAL_COMPONENT = "26"  # Professional component
    TECHNICAL_COMPONENT = "TC"  # Technical component


class CPTCode(BaseModel):
    """Domain model for CPT (Current Procedural Terminology) codes"""
    
    code: str = Field(..., description="CPT code (5-digit numeric code)", pattern=r"^\d{5}$")
    description: str = Field(..., description="Full description of the procedure/service")
    short_description: Optional[str] = Field(None, description="Abbreviated description")
    
    # Classification
    category: Optional[CPTCategory] = Field(None, description="CPT category")
    
    # Modifiers
    modifiers: Optional[List[CPTModifier]] = Field(None, description="CPT modifiers applied")
    modifier_descriptions: Optional[List[str]] = Field(None, description="Descriptions of applied modifiers")
    
    # Clinical context
    units: int = Field(1, ge=1, description="Number of units/times procedure performed")
    laterality: Optional[str] = Field(None, description="Left, Right, or Bilateral")
    
    # Billing information
    rvu: Optional[float] = Field(None, description="Relative Value Units")
    fee_schedule_amount: Optional[float] = Field(None, description="Fee schedule amount in USD")
    is_bundled: bool = Field(False, description="Whether this is part of a bundled service")
    requires_prior_auth: bool = Field(False, description="Whether prior authorization is required")
    
    # AI metadata
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI confidence in code selection")
    extracted_from_text: Optional[str] = Field(None, description="Text snippet that led to this code")
    alternative_codes: Optional[List[str]] = Field(None, description="Alternative CPT codes considered")
    
    # Associated diagnosis codes
    linked_icd10_codes: Optional[List[str]] = Field(None, description="Associated ICD-10 diagnosis codes")
    
    # Metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when code was assigned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "99213",
                "description": "Office or other outpatient visit, established patient, 20-29 minutes",
                "short_description": "Office visit - established patient",
                "category": "99201-99499",
                "modifiers": ["25"],
                "modifier_descriptions": ["Significant, separately identifiable E&M service"],
                "units": 1,
                "confidence_score": 0.93,
                "requires_prior_auth": False,
                "linked_icd10_codes": ["E11.9", "I10"]
            }
        }


class CPTCodeSet(BaseModel):
    """Collection of CPT codes for a patient encounter"""
    
    encounter_id: Optional[str] = Field(None, description="Associated encounter/visit ID")
    patient_id: Optional[str] = Field(None, description="Patient identifier")
    provider_id: Optional[str] = Field(None, description="Provider identifier")
    service_date: Optional[datetime] = Field(None, description="Date of service")
    
    codes: List[CPTCode] = Field(..., description="List of CPT codes")
    
    # Billing summary
    total_rvu: Optional[float] = Field(None, description="Total RVUs for all procedures")
    estimated_total_charge: Optional[float] = Field(None, description="Estimated total charge in USD")
    
    # AI generation metadata
    generated_by_ai: bool = Field(False, description="Whether codes were AI-generated")
    ai_provider: Optional[str] = Field(None, description="AI provider used")
    source_text: Optional[str] = Field(None, description="Source text used for code generation")
    
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "encounter_id": "ENC001",
                "patient_id": "P12345",
                "provider_id": "DR001",
                "service_date": "2024-11-28T10:30:00Z",
                "codes": [
                    {
                        "code": "99213",
                        "description": "Office visit - established patient",
                        "category": "99201-99499",
                        "units": 1,
                        "confidence_score": 0.93
                    },
                    {
                        "code": "80053",
                        "description": "Comprehensive metabolic panel",
                        "category": "80047-89398",
                        "units": 1,
                        "confidence_score": 0.88
                    }
                ],
                "generated_by_ai": True,
                "ai_provider": "aws"
            }
        }


class MedicalCodeRequest(BaseModel):
    """Request model for generating medical codes (both ICD-10 and CPT)"""
    text: str = Field(..., description="Input text to extract medical codes from")
    patient_id: Optional[str] = Field(None, description="Optional patient identifier")
    encounter_id: Optional[str] = Field(None, description="Optional encounter identifier")
    include_icd10: bool = Field(True, description="Whether to generate ICD-10 codes")
    include_cpt: bool = Field(True, description="Whether to generate CPT codes")
    include_confidence: bool = Field(True, description="Whether to include confidence scores")


class MedicalCodeResponse(BaseModel):
    """Response model for medical code generation"""
    icd10_codes: Optional[List[dict]] = Field(None, description="Generated ICD-10 codes")
    cpt_codes: Optional[List[dict]] = Field(None, description="Generated CPT codes")
    provider: str = Field(..., description="AI provider used for generation")
    processing_time_ms: Optional[float] = Field(None, description="Time taken to generate codes")
