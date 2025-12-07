import boto3
import os
from langchain_aws import ChatBedrock
from app.core.config import settings

print(f"User Profile: {os.environ.get('USERPROFILE')}")
print(f"Home: {os.environ.get('HOME')}")
print(f"Settings Model: {settings.BEDROCK_MODEL_ID}")
print(f"Settings Region: {settings.AWS_REGION}")

try:
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print(f"Boto3 Identity: {identity['Arn']}")
except Exception as e:
    print(f"Boto3 failed: {e}")

try:
    print("Test 1: Hardcoded problematic model")
    chat = ChatBedrock(
        model_id="openai.gpt-oss-120b-1:0",
        region_name="us-east-1",
        model_kwargs={"temperature": 0.0}
    )
    print("Test 1: SUCCESS")
except Exception as e:
    print(f"Test 1 FAILED: {e}")

try:
    print("Test 3: AWS_PROFILE env var")
    os.environ["AWS_PROFILE"] = "default"
    chat = ChatBedrock(
        model_id="openai.gpt-oss-120b-1:0",
        region_name="us-east-1",
        model_kwargs={"temperature": 0.0}
    )
    print("Test 3: SUCCESS")
except Exception as e:
    print(f"Test 3 FAILED: {e}")
