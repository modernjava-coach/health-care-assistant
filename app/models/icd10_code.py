from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ICD10Category(str, Enum):
    """ICD-10 code categories"""
    INFECTIOUS_DISEASES = "A00-B99"
    NEOPLASMS = "C00-D49"
    BLOOD_DISORDERS = "D50-D89"
    ENDOCRINE = "E00-E89"
    MENTAL_BEHAVIORAL = "F01-F99"
    NERVOUS_SYSTEM = "G00-G99"
    EYE = "H00-H59"
    EAR = "H60-H95"
    CIRCULATORY = "I00-I99"
    RESPIRATORY = "J00-J99"
    DIGESTIVE = "K00-K95"
    SKIN = "L00-L99"
    MUSCULOSKELETAL = "M00-M99"
    GENITOURINARY = "N00-N99"
    PREGNANCY = "O00-O9A"
    PERINATAL = "P00-P96"
    CONGENITAL = "Q00-Q99"
    SYMPTOMS = "R00-R99"
    INJURY = "S00-T88"
    EXTERNAL_CAUSES = "V00-Y99"
    HEALTH_STATUS = "Z00-Z99"


class ICD10CodeType(str, Enum):
    """ICD-10 code types"""
    DIAGNOSIS = "diagnosis"
    SYMPTOM = "symptom"
    PROCEDURE = "procedure"
    EXTERNAL_CAUSE = "external_cause"


class ICD10Code(BaseModel):
    """Domain model for ICD-10 (International Classification of Diseases, 10th Revision) codes"""
    
    code: str = Field(..., description="ICD-10 code (e.g., E11.9, J44.0)", pattern=r"^[A-Z][0-9]{2}(\.[0-9]{1,4})?$")
    description: str = Field(..., description="Full description of the diagnosis/condition")
    short_description: Optional[str] = Field(None, description="Abbreviated description")
    
    # Classification
    category: Optional[ICD10Category] = Field(None, description="ICD-10 category range")
    code_type: ICD10CodeType = Field(default=ICD10CodeType.DIAGNOSIS, description="Type of ICD-10 code")
    
    # Clinical context
    is_primary: bool = Field(False, description="Whether this is the primary diagnosis")
    is_chronic: Optional[bool] = Field(None, description="Whether this is a chronic condition")
    severity: Optional[str] = Field(None, description="Severity level (mild, moderate, severe)")
    
    # AI metadata
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI confidence in code selection")
    extracted_from_text: Optional[str] = Field(None, description="Text snippet that led to this code")
    alternative_codes: Optional[List[str]] = Field(None, description="Alternative ICD-10 codes considered")
    
    # Billing and administrative
    billable: Optional[bool] = Field(None, description="Whether this code is billable")
    requires_additional_digits: bool = Field(False, description="Whether more specific code is needed")
    
    # Metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when code was assigned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "E11.9",
                "description": "Type 2 diabetes mellitus without complications",
                "short_description": "Type 2 diabetes",
                "category": "E00-E89",
                "code_type": "diagnosis",
                "is_primary": True,
                "is_chronic": True,
                "severity": "moderate",
                "confidence_score": 0.95,
                "billable": True,
                "requires_additional_digits": False
            }
        }


class ICD10CodeSet(BaseModel):
    """Collection of ICD-10 codes for a patient encounter"""
    
    encounter_id: Optional[str] = Field(None, description="Associated encounter/visit ID")
    patient_id: Optional[str] = Field(None, description="Patient identifier")
    codes: List[ICD10Code] = Field(..., description="List of ICD-10 codes")
    primary_code: Optional[str] = Field(None, description="Primary diagnosis code")
    
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
                "codes": [
                    {
                        "code": "E11.9",
                        "description": "Type 2 diabetes mellitus without complications",
                        "is_primary": True,
                        "confidence_score": 0.95
                    },
                    {
                        "code": "I10",
                        "description": "Essential (primary) hypertension",
                        "is_primary": False,
                        "confidence_score": 0.92
                    }
                ],
                "primary_code": "E11.9",
                "generated_by_ai": True,
                "ai_provider": "aws"
            }
        }
