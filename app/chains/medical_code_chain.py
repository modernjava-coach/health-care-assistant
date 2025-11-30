from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from ..models import MedicalCodeResponse
from ..core.config import settings
import re

def strip_reasoning_tags(text: str) -> str:
    """Remove <reasoning> tags from OpenAI model output."""
    cleaned = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL)
    return cleaned.strip()

def get_medical_code_chain(model_id: str = None, region_name: str = None):
    model_id = model_id or settings.BEDROCK_MODEL_ID
    region_name = region_name or settings.AWS_REGION
    
    llm = ChatBedrock(
        model_id=model_id,
        region_name=region_name,
        model_kwargs={"temperature": 0.0}
    )
    
    parser = PydanticOutputParser(pydantic_object=MedicalCodeResponse)
    
    system_template = """You are a certified medical coder. Extract ICD-10 and CPT codes from the clinical text.
    
    {format_instructions}
    
    IMPORTANT: Return ONLY the JSON object. Do not include any reasoning, explanations, or XML tags."""
    
    human_template = "{text}"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template)
    ]).partial(format_instructions=parser.get_format_instructions())
    
    # Add preprocessing step to strip reasoning tags
    preprocess = RunnableLambda(lambda x: strip_reasoning_tags(x.content))
    
    chain = prompt | llm | preprocess | parser
    return chain

