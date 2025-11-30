# AWS Bedrock Model Setup Guide

## Overview
AWS Bedrock requires you to explicitly request access to foundation models before you can use them via the API. This guide walks you through enabling the models needed for this medical assistant application.

## Current Model Configuration
The application currently uses:
- **Primary Model**: `anthropic.claude-3-5-sonnet-20240620-v1:0` (Claude 3.5 Sonnet)
- **Region**: `us-east-1` (configurable)

## Step-by-Step: Enable Models in AWS Console

### 1. Access the Bedrock Console
1. Log into your AWS Console
2. Navigate to **Amazon Bedrock** service
3. Select your region (e.g., `us-east-1`)

### 2. Request Model Access
1. In the left sidebar, click **Model access**
2. Click **Manage model access** (orange button in top right)
3. You'll see a list of available foundation models

### 3. Enable Anthropic Claude Models
For this application, you need to enable:

#### Required Models:
- ✅ **Claude 3.5 Sonnet** (`anthropic.claude-3-5-sonnet-20240620-v1:0`)
  - Best for production use
  - High accuracy for medical documentation
  - Recommended for SOAP notes and medical coding

#### Optional Models (for testing/comparison):
- **Claude 3 Opus** (`anthropic.claude-3-opus-20240229-v1:0`)
  - Highest capability, slower and more expensive
- **Claude 3 Sonnet** (`anthropic.claude-3-sonnet-20240229-v1:0`)
  - Good balance of speed and quality
- **Claude 3 Haiku** (`anthropic.claude-3-haiku-20240307-v1:0`)
  - Fastest and cheapest, lower quality

### 4. Submit Access Request
1. Check the boxes next to the models you want
2. Review the End User License Agreements (EULAs)
3. Click **Request model access**

### 5. Wait for Approval
- **Anthropic Claude models**: Usually instant approval
- You'll see status change from "Requesting" to "Access granted"
- Some models may require manual approval (1-2 business days)

### 6. Verify Access
Run the provided Python script to verify your access:
```bash
python scripts/check_bedrock_access.py
```

## Available Regions
Bedrock is available in these regions (as of 2024):
- `us-east-1` (N. Virginia) - Recommended, most models available
- `us-west-2` (Oregon)
- `ap-southeast-1` (Singapore)
- `ap-northeast-1` (Tokyo)
- `eu-central-1` (Frankfurt)
- `eu-west-3` (Paris)

> [!IMPORTANT]
> Model availability varies by region. Claude 3.5 Sonnet is available in `us-east-1` and `us-west-2`.

## Pricing Considerations
Anthropic Claude 3.5 Sonnet pricing (as of Nov 2024):
- **Input**: $3.00 per million tokens
- **Output**: $15.00 per million tokens

For typical medical documentation:
- SOAP note generation: ~500-1000 input tokens, ~300-500 output tokens
- Medical coding: ~300-600 input tokens, ~200-400 output tokens
- Estimated cost per request: $0.01 - $0.02

## Troubleshooting

### Error: "AccessDeniedException"
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException) 
when calling the InvokeModel operation: You don't have access to the model
```

**Solution**: You haven't enabled the model in Bedrock console. Follow steps above.

### Error: "ValidationException: The provided model identifier is invalid"
```
botocore.exceptions.ClientError: An error occurred (ValidationException)
```

**Solution**: 
1. Check the model ID is correct
2. Verify the model is available in your region
3. Ensure you're using the correct model version

### Error: "ThrottlingException"
```
botocore.exceptions.ClientError: An error occurred (ThrottlingException)
```

**Solution**: You've exceeded the rate limit. Implement exponential backoff or request a quota increase.

## AWS Credentials Setup

Ensure your AWS credentials are configured:

### Option 1: AWS CLI Configuration
```bash
aws configure
```

### Option 2: Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Option 3: IAM Role (for EC2/ECS)
Attach an IAM role with the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
      ]
    }
  ]
}
```

## Testing Your Setup

After enabling models, test with:

```python
from app.providers.bedrock import BedrockProvider

# Initialize provider
provider = BedrockProvider(region_name="us-east-1")

# Test SOAP note generation
test_text = """
Patient presents with fever of 101.5F for 2 days, 
productive cough with yellow sputum, and fatigue.
Lungs show crackles in right lower lobe.
"""

soap_note = provider.generate_soap_note(test_text)
print(soap_note.model_dump_json(indent=2))
```

## Next Steps

1. ✅ Enable Claude 3.5 Sonnet in AWS Bedrock Console
2. ✅ Configure AWS credentials
3. ✅ Run verification script
4. ✅ Test with sample medical text
5. 📝 Consider enabling additional models for comparison

## Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Claude Models](https://docs.anthropic.com/claude/docs)
- [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Model Access Management](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
