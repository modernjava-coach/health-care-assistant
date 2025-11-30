# AWS Bedrock Model Setup

This directory contains scripts to help you enable and verify AWS Bedrock model access.

## Quick Start

### Option 1: Interactive Setup (Recommended)
```bash
python scripts/setup_bedrock.py
```

This will:
- Check your AWS CLI configuration
- Display step-by-step instructions
- Optionally run the verification script

### Option 2: Direct Verification
```bash
python scripts/check_bedrock_access.py
```

This will check which models you have access to and provide detailed status.

## What You Need to Do

1. **Enable Models in AWS Console**
   - Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
   - Click "Model access" in the left sidebar
   - Click "Manage model access"
   - Enable **Claude 3.5 Sonnet** (required)
   - Click "Request model access"

2. **Verify Access**
   ```bash
   python scripts/check_bedrock_access.py
   ```

3. **Test Your Application**
   ```bash
   python -m pytest tests/test_api_bedrock.py
   ```

## Detailed Documentation

See [BEDROCK_SETUP.md](../BEDROCK_SETUP.md) for:
- Complete step-by-step instructions
- Troubleshooting guide
- AWS credentials setup
- Pricing information
- Regional availability

## Required Model

Your application requires:
- **Claude 3.5 Sonnet** (`anthropic.claude-3-5-sonnet-20240620-v1:0`)

This model is used for:
- SOAP note generation
- Medical coding (ICD-10 and CPT codes)

## Optional Models

You can also enable these for testing:
- Claude 3 Sonnet (good balance)
- Claude 3 Haiku (fastest, cheapest)
- Claude 3 Opus (highest quality)

## Troubleshooting

### "AccessDeniedException"
You haven't enabled the model in Bedrock console. Follow the steps above.

### "AWS credentials not configured"
Run `aws configure` or set environment variables:
```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"
```

### Model not available in your region
Claude 3.5 Sonnet is available in:
- `us-east-1` (recommended)
- `us-west-2`

Change region in the BedrockProvider initialization or use:
```bash
python scripts/check_bedrock_access.py --region us-west-2
```

## Next Steps

After enabling models:
1. ✅ Run verification script
2. ✅ Test with sample medical text
3. ✅ Run the test suite
4. 🚀 Start using the application!
