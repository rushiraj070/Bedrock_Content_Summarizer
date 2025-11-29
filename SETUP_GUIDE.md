# Complete Setup Guide

## Prerequisites

- Python 3.8 or higher
- AWS Account with Bedrock access
- IAM user with appropriate permissions

## Step-by-Step Setup

### 1. Install Dependencies

All required packages are already installed in your environment:
- ✓ boto3 (AWS SDK)
- ✓ streamlit (Web framework)

If you need to reinstall:
```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

#### Option A: Environment Variables (Recommended for Development)

**Windows (CMD):**
```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=us-east-1
```

**Windows (PowerShell):**
```powershell
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:AWS_DEFAULT_REGION="us-east-1"
```

**Linux/Mac:**
```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1
```

#### Option B: AWS CLI Configuration

```bash
aws configure
```

#### Option C: IAM Role (For EC2/ECS)

If running on AWS infrastructure, attach an IAM role with Bedrock permissions.

### 3. Verify AWS Setup

Test your connection:
```bash
python bedrock_setup.py
```

Expected output:
```
✓ Connected to Bedrock in region: us-east-1
✓ Found X available models
```

### 4. Launch the Application

#### Quick Launch (Windows):
```cmd
run_app.bat
```

#### Manual Launch:
```bash
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 5. Using the Application

1. **Check Credentials**: Sidebar shows credential status
2. **Select Configuration**: Choose AWS region and Claude model
3. **Input Text**: 
   - Type/paste directly
   - Upload a `.txt` or `.md` file
   - Use the sample text
4. **Generate**: Click "Generate Summaries"
5. **Review**: Expand each summary section
6. **Download**: Export all summaries as a text file

## IAM Permissions Setup

### Minimum Required Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvokeModel",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-opus-20240229-v1:0"
      ]
    }
  ]
}
```

### Creating IAM User

1. Go to AWS IAM Console
2. Create new user: `bedrock-summarizer-user`
3. Attach the policy above
4. Create access keys
5. Save credentials securely

## Model Availability by Region

| Region | Code | Claude 3 Haiku | Claude 3 Sonnet | Claude 3 Opus |
|--------|------|----------------|-----------------|---------------|
| US East (N. Virginia) | us-east-1 | ✓ | ✓ | ✓ |
| US West (Oregon) | us-west-2 | ✓ | ✓ | ✓ |
| EU (Frankfurt) | eu-central-1 | ✓ | ✓ | ✗ |
| Asia Pacific (Singapore) | ap-southeast-1 | ✓ | ✓ | ✗ |

**Recommendation**: Use `us-east-1` for full model availability.

## Troubleshooting

### Issue: "AWS credentials not configured"

**Solution:**
- Verify environment variables are set in current terminal
- Check spelling of variable names
- Restart terminal after setting variables

**Test:**
```bash
echo %AWS_ACCESS_KEY_ID%  # Windows CMD
echo $env:AWS_ACCESS_KEY_ID  # Windows PowerShell
echo $AWS_ACCESS_KEY_ID  # Linux/Mac
```

### Issue: "AccessDeniedException"

**Solution:**
- Verify IAM policy includes `bedrock:InvokeModel`
- Check resource ARN matches your region
- Ensure model is available in selected region

**Test:**
```bash
aws bedrock list-foundation-models --region us-east-1
```

### Issue: "Model not found"

**Solution:**
- Model may not be available in your region
- Try `us-east-1` or `us-west-2`
- Check AWS Bedrock console for model availability
- Verify model ID spelling

### Issue: "Streamlit won't start"

**Solution:**
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check port 8501 is not in use
- Try different port: `streamlit run streamlit_app.py --server.port 8502`

### Issue: "Connection timeout"

**Solution:**
- Check internet connectivity
- Verify AWS region is accessible
- Check firewall/proxy settings
- Try different AWS region

## Performance Optimization

### Model Selection

- **Claude 3 Haiku**: Best for speed and cost (default)
  - ~1-2 seconds per summary
  - $0.25/$1.25 per million tokens (input/output)
  
- **Claude 3 Sonnet**: Balanced quality and speed
  - ~2-4 seconds per summary
  - $3/$15 per million tokens
  
- **Claude 3 Opus**: Best quality
  - ~4-8 seconds per summary
  - $15/$75 per million tokens

### Cost Estimation

For a 1,000-word article:
- Haiku: ~$0.005 per summarization (all 3 lengths)
- Sonnet: ~$0.025 per summarization
- Opus: ~$0.125 per summarization

### Batch Processing

For processing multiple documents:
1. Add rate limiting (avoid throttling)
2. Use Haiku for initial processing
3. Use Sonnet/Opus for important documents only

## Advanced Configuration

### Custom Model Parameters

Edit `main.py` to adjust:

```python
# Temperature (0.0-1.0): Lower = more focused, Higher = more creative
"temperature": 0.5,

# Top P (0.0-1.0): Nucleus sampling threshold
"top_p": 0.9,

# Max tokens: Maximum length of generated summary
"max_tokens": 300
```

### Custom Summary Lengths

Modify `length_params` in `main.py`:

```python
length_params = {
    'short': {
        'description': 'your custom description',
        'max_tokens': 100
    },
    # ... add more lengths
}
```

## Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
```

### Production Deployment

#### AWS EC2
1. Launch EC2 instance with IAM role
2. Install dependencies
3. Run with: `streamlit run streamlit_app.py --server.port 80`

#### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

#### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add AWS credentials in secrets

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use IAM roles** when possible (EC2, ECS, Lambda)
3. **Rotate access keys** regularly
4. **Use least privilege** IAM policies
5. **Enable CloudTrail** for audit logging
6. **Monitor costs** with AWS Budgets

## Getting Help

- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- Streamlit Documentation: https://docs.streamlit.io/
- Claude Model Cards: https://www.anthropic.com/claude

## Next Steps

1. ✓ Complete setup and test with sample text
2. Try different Claude models
3. Process your own documents
4. Customize summary parameters
5. Deploy to production environment
