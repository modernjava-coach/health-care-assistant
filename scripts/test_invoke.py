import boto3
import json

def test_invoke():
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = "openai.gpt-oss-20b-1:0"
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello, are you working?"
            }
        ],
        "max_tokens": 100
    }
    
    try:
        print(f"Attempting to invoke {model_id}...")
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload)
        )
        response_body = json.loads(response.get("body").read())
        print("Success!")
        print(response_body)
    except Exception as e:
        print(f"Error invoking model: {e}")

if __name__ == "__main__":
    test_invoke()
