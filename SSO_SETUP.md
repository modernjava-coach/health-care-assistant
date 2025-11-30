# AWS SSO Configuration Guide

## Overview
AWS IAM Identity Center (formerly AWS SSO) is the recommended way to manage AWS access. This guide helps you configure the AWS CLI to use SSO.

## Prerequisites
- AWS CLI version 2 installed
- Your AWS SSO Start URL (e.g., `https://my-company.awsapps.com/start`)
- Your AWS SSO Region (e.g., `us-east-1`)

## Step-by-Step Configuration

### 1. Run the Configuration Command
Open your terminal and run:

```bash
aws configure sso
```

### 2. Follow the Prompts

You will be asked for the following information:

1.  **SSO Start URL**: Enter your provided URL
    - Example: `https://d-1234567890.awsapps.com/start`
    
2.  **SSO Region**: Enter the region where SSO is configured
    - Example: `us-east-1`

3.  **Browser Login**: 
    - The CLI will open your default browser
    - Log in with your corporate credentials
    - Allow the access request

4.  **Account Selection**:
    - Select the AWS account you want to access
    - Select the Role (e.g., `AdministratorAccess`, `PowerUserAccess`)

5.  **CLI Profile Configuration**:
    - **CLI default client Region**: `us-east-1` (or your preferred region)
    - **CLI default output format**: `json`
    - **CLI profile name**: Enter a name (e.g., `bedrock-dev` or leave default)

### 3. Using the Profile

Once configured, you can run commands using the profile:

```bash
aws s3 ls --profile bedrock-dev
```

Or set it as the default for your session:

**Windows (PowerShell):**
```powershell
$env:AWS_PROFILE = "bedrock-dev"
```

**Mac/Linux:**
```bash
export AWS_PROFILE=bedrock-dev
```

## Refreshing Credentials

SSO credentials expire periodically (usually 8-12 hours). To login again:

```bash
aws sso login --profile bedrock-dev
```

## Troubleshooting

### "Invalid choice: 'sso'"
Your AWS CLI version might be too old. Check version:
```bash
aws --version
```
You need AWS CLI v2.

### Browser doesn't open
If the browser doesn't open automatically, the CLI will print a URL and a code. Open the URL manually and enter the code.
