# Amazon Bedrock Content Summarizer

A powerful web application that generates AI-powered text summaries using Amazon Bedrock's Claude models. Get short, medium, and long summaries of any text with a beautiful Streamlit interface.

## Features

- 🎯 **Three Summary Lengths**: Short (2-3 sentences), Medium (1 paragraph), Long (detailed)
- 🚀 **Multiple Input Methods**: Type/paste text, upload files, or use sample text
- 🎨 **Beautiful UI**: Clean, modern Streamlit interface
- 📊 **Text Statistics**: Character, word, and line counts
- 💾 **Export Results**: Download all summaries as a text file
- 🔧 **Flexible Configuration**: Choose AWS region and Claude model
- ⚡ **Fast & Cost-Effective**: Uses Claude 3 Haiku by default

## Project Structure

```
Bedrock_Content_Summarizer/
│
├── main.py                      # Core summarization logic
├── streamlit_app.py             # Web interface
├── requirements.txt             # Python dependencies
├── architecture_diagram.mmd     # Mermaid architecture diagram
├── README.md                    # This file
├── samples/
│   └── sample-text.txt         # Sample text for testing
└── assets/
    └── screenshots/            # App screenshots
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Set your AWS credentials as environment variables:

```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=us-east-1
```

### 3. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### 4. Start Summarizing!

1. Choose your input method (type, upload, or use sample)
2. Enter or load your text
3. Click "Generate Summaries"
4. View and download your results

## AWS Configuration

### Required IAM Permissions

Your IAM user needs:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/*"
    }
  ]
}
```

### Supported Regions

- `us-east-1` (N. Virginia) - Recommended
- `us-west-2` (Oregon)
- `eu-central-1` (Frankfurt)
- `ap-southeast-1` (Singapore)

### Available Models

- **Claude 3 Haiku**: Fast and economical (default)
- **Claude 3 Sonnet**: Balanced performance and quality
- **Claude 3 Opus**: Best quality, higher cost

## Usage

### Web Interface

The Streamlit app provides an intuitive interface:

1. **Configuration Sidebar**: Select AWS region and Claude model
2. **Input Methods**:
   - Type or paste text directly
   - Upload `.txt` or `.md` files
   - Use the provided sample text
3. **Generate Summaries**: Click the button to process
4. **View Results**: Expandable sections for each summary length
5. **Download**: Export all summaries as a text file

### Programmatic Usage

You can also use the core module in your own Python code:

```python
from main import BedrockSummarizer

# Initialize
summarizer = BedrockSummarizer(
    region='us-east-1',
    model_id='anthropic.claude-3-haiku-20240307-v1:0'
)

# Generate all summaries
summaries = summarizer.summarize_all_lengths("Your text here...")
print(summaries['short'])
print(summaries['medium'])
print(summaries['long'])

# Or generate a specific length
short_summary = summarizer.generate_summary("Your text here...", 'short')
```


## Architecture

The application follows a clean, modular architecture:

```
User Input → Streamlit UI → BedrockSummarizer → AWS Bedrock → Claude Model
                ↓                                      ↓
           Text Stats                            Summaries (3 lengths)
                ↓                                      ↓
           Display & Download ← ← ← ← ← ← ← ← ← ← ← ←
```

See `architecture_diagram.mmd` for a detailed Mermaid diagram.

## Cost Considerations

Claude 3 Haiku pricing (approximate):
- **Input**: $0.25 per million tokens (~750,000 words)
- **Output**: $1.25 per million tokens

**Example**: Summarizing a 1,000-word article costs less than $0.01

## Troubleshooting

### "AWS credentials not configured"
- Ensure environment variables are set in your current terminal session
- Verify credentials are valid using `aws sts get-caller-identity`

### "AccessDeniedException"
- Check IAM permissions include `bedrock:InvokeModel`
- Verify the model is available in your selected region

### "Model not found"
- Claude 3 models may not be available in all regions
- Try `us-east-1` or `us-west-2`
- Check AWS Bedrock console for model availability

### Streamlit won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## Development

### Running Tests

```bash
python bedrock_setup.py
```

### Project Dependencies

- `boto3`: AWS SDK for Python
- `streamlit`: Web application framework
- Python 3.8 or higher

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and commercial use.

## Acknowledgments

- Built with Amazon Bedrock and Claude 3 models
- UI powered by Streamlit
- AWS SDK provided by boto3
