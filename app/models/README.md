# Domain Models for Medical Assistant

This directory contains comprehensive domain models for medical data:

## Models

### 1. SOAP Notes (`soap_note.py`)
SOAP (Subjective, Objective, Assessment, Plan) notes are the standard format for medical documentation.

**Key Models:**
- `SOAPNote`: Complete SOAP note with all components
- `SOAPNoteType`: Enum for note types (initial consultation, follow-up, emergency, routine checkup)
- `SOAPNoteRequest`: Request model for generating SOAP notes
- `SOAPNoteResponse`: Response model with generated SOAP note

**Features:**
- Structured S.O.A.P. components
- Patient and provider tracking
- Vital signs integration
- AI generation metadata (provider, confidence score)
- Timestamps for audit trail

### 2. ICD-10 Codes (`icd10_code.py`)
ICD-10 (International Classification of Diseases, 10th Revision) codes for diagnoses.

**Key Models:**
- `ICD10Code`: Individual diagnosis code with full metadata
- `ICD10CodeSet`: Collection of codes for an encounter
- `ICD10Category`: Enum for major disease categories (A00-Z99)
- `ICD10CodeType`: Enum for code types (diagnosis, symptom, procedure, external cause)

**Features:**
- Code validation with regex pattern
- Category classification (21 major categories)
- Clinical context (primary/secondary, chronic, severity)
- Billing information (billable status)
- AI confidence scores and alternatives
- Text extraction tracking

### 3. CPT Codes (`cpt_code.py`)
CPT (Current Procedural Terminology) codes for medical procedures and services.

**Key Models:**
- `CPTCode`: Individual procedure code with modifiers
- `CPTCodeSet`: Collection of codes for an encounter
- `CPTCategory`: Enum for procedure categories (E&M, Surgery, Lab, etc.)
- `CPTModifier`: Enum for common modifiers (bilateral, multiple procedures, etc.)
- `MedicalCodeRequest`: Unified request for both ICD-10 and CPT codes
- `MedicalCodeResponse`: Unified response with both code types

**Features:**
- 5-digit code validation
- Comprehensive modifier support (25+ common modifiers)
- Billing information (RVU, fee schedules)
- Units and laterality tracking
- Prior authorization flags
- Linked diagnosis codes (ICD-10)
- AI confidence and alternatives

## Usage

Import models from the package:

```python
from app.models import (
    SOAPNote, SOAPNoteType, SOAPNoteRequest, SOAPNoteResponse,
    ICD10Code, ICD10CodeSet, ICD10Category, ICD10CodeType,
    CPTCode, CPTCodeSet, CPTCategory, CPTModifier,
    MedicalCodeRequest, MedicalCodeResponse
)
```

See `examples/model_usage_examples.py` for detailed usage examples.

## Validation

All models use Pydantic for:
- Type validation
- Field constraints (regex patterns, value ranges)
- Automatic serialization/deserialization
- JSON schema generation
- Example data in schema

## AI Integration

All models include fields for AI generation tracking:
- `generated_by_ai`: Boolean flag
- `ai_provider`: Provider name (aws, google, etc.)
- `confidence_score`: 0.0-1.0 confidence level
- `extracted_from_text`: Source text snippet
- `alternative_codes`: Other codes considered

## Medical Coding Standards

### ICD-10 Format
- Pattern: `[A-Z][0-9]{2}(\.[0-9]{1,4})?`
- Examples: `E11.9`, `I10`, `J44.0`
- Categories: A00-Z99 (21 major categories)

### CPT Format
- Pattern: `\d{5}` (5-digit numeric)
- Examples: `99213`, `80053`, `70450`
- Categories: 00100-99607
- Modifiers: 2-digit or 2-character codes

## Best Practices

1. **Always link CPT codes to ICD-10 codes** for proper billing
2. **Use primary diagnosis flag** to indicate main diagnosis
3. **Include confidence scores** when using AI generation
4. **Track source text** for audit and verification
5. **Apply appropriate modifiers** to CPT codes
6. **Validate billable status** before submitting claims
