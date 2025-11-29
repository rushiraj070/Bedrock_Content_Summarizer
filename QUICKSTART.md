# Quick Start Guide

## Step 1: Configure AWS Credentials

Set your AWS credentials in the current terminal session:

```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=us-east-1
```

## Step 2: Test Connection

```cmd
python bedrock_setup.py
```

This will verify your credentials and list available Bedrock models.

## Step 3: Run the Summarizer

### With sample text:
```cmd
python bedrock_summarizer.py sample_text.txt
```

### With your own text file:
```cmd
python bedrock_summarizer.py your_document.txt
```

### Without arguments (uses built-in sample):
```cmd
python bedrock_summarizer.py
```

## Troubleshooting

### "AWS credentials not configured"
- Make sure you've set the environment variables in your current terminal
- Check that your credentials are valid

### "AccessDeniedException"
- Ensure your IAM user has these permissions:
  - `bedrock:InvokeModel`
  - `bedrock:ListFoundationModels`

### "Model not found"
- Claude 3 Haiku may not be available in your region
- Try changing the region to `us-east-1` or `us-west-2`
- Or modify the `modelId` in `bedrock_summarizer.py`

## Cost Considerations

Claude 3 Haiku pricing (approximate):
- Input: $0.25 per million tokens
- Output: $1.25 per million tokens

A typical summarization of 1000 words costs less than $0.01.

## Next Steps

1. Modify `bedrock_summarizer.py` to customize:
   - Summary lengths and descriptions
   - Model selection (try Claude 3 Sonnet for better quality)
   - Temperature and other parameters
   - Output format

2. Integrate into your applications:
   - Import the `BedrockSummarizer` class
   - Use `generate_summary()` or `summarize_all_lengths()` methods
   - Handle exceptions appropriately

3. Explore other Bedrock models:
   - Claude 3 Sonnet: Better quality, higher cost
   - Claude 3 Opus: Best quality, highest cost
   - Other providers: AI21, Cohere, Meta Llama
