import boto3
import json

def list_bedrock_models():
    try:
        client = boto3.client('bedrock', region_name='us-east-1')
        response = client.list_foundation_models()
        
        print("Searching for OpenAI/GPT models in Bedrock:")
        found = False
        for model in response.get('modelSummaries', []):
            if 'openai' in model['modelId'].lower() or 'gpt' in model['modelId'].lower():
                print(f"Name: {model['modelName']}")
                print(f"ID: {model['modelId']}")
                print(f"Provider: {model['providerName']}")
                print(f"Status: {model.get('modelLifecycle', {}).get('status', 'Unknown')}")
                print("-" * 30)
                found = True
        
        if not found:
            print("No OpenAI or GPT models found in the list.")
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_bedrock_models()
