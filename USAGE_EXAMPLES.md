# Usage Examples

## Example 1: Basic Usage with Sample File

```cmd
python bedrock_summarizer.py sample_text.txt
```

**Output:**
```
================================================================================
AMAZON BEDROCK TEXT SUMMARIZER
================================================================================

📂 Loading text from: sample_text.txt

✓ Connected to Bedrock in region: us-east-1

🔄 Generating short summary...
✓ Short summary complete
🔄 Generating medium summary...
✓ Medium summary complete
🔄 Generating long summary...
✓ Long summary complete

================================================================================
SUMMARIZATION RESULTS
================================================================================

📄 Original Text Length: 1523 characters
   Word Count: 234 words

--------------------------------------------------------------------------------
SHORT SUMMARY (2-3 sentences)
--------------------------------------------------------------------------------
[Your short summary appears here]

   Length: 145 characters

[... medium and long summaries follow ...]
```

## Example 2: Using Your Own Text File

Create a file called `my_article.txt` with your content, then:

```cmd
python bedrock_summarizer.py my_article.txt
```

## Example 3: Using Without Arguments (Built-in Sample)

```cmd
python bedrock_summarizer.py
```

This uses a built-in sample text about AI for quick testing.

## Example 4: Using as a Python Module

```python
from bedrock_summarizer import BedrockSummarizer

# Initialize
summarizer = BedrockSummarizer(region='us-east-1')

# Your text
text = "Your long article or document text here..."

# Get all three summaries
summaries = summarizer.summarize_all_lengths(text)
print(summaries['short'])
print(summaries['medium'])
print(summaries['long'])

# Or get just one specific length
short_only = summarizer.generate_summary(text, 'short')
print(short_only)
```

## Example 5: Batch Processing Multiple Files

Create a batch script `summarize_all.bat`:

```batch
@echo off
for %%f in (*.txt) do (
    echo Processing %%f...
    python bedrock_summarizer.py "%%f" > "%%f_summary.txt"
)
```

## Example 6: Customizing Summary Parameters

Edit `bedrock_summarizer.py` to change summary characteristics:

```python
length_params = {
    'short': {
        'description': '1 sentence only',  # Changed from 2-3
        'max_tokens': 100                   # Reduced from 150
    },
    'medium': {
        'description': '2-3 sentences',     # Changed from 1 paragraph
        'max_tokens': 200                   # Reduced from 300
    },
    'long': {
        'description': '1-2 paragraphs',    # Changed from multiple
        'max_tokens': 400                   # Reduced from 600
    }
}
```

## Example 7: Using Different Claude Models

In `bedrock_summarizer.py`, change the model ID:

```python
# For better quality (higher cost):
modelId='anthropic.claude-3-sonnet-20240229-v1:0'

# For best quality (highest cost):
modelId='anthropic.claude-3-opus-20240229-v1:0'

# Current (fast and economical):
modelId='anthropic.claude-3-haiku-20240307-v1:0'
```

## Example 8: Error Handling in Your Code

```python
from bedrock_summarizer import BedrockSummarizer

try:
    summarizer = BedrockSummarizer(region='us-east-1')
    summary = summarizer.generate_summary(text, 'short')
    print(f"Summary: {summary}")
except Exception as e:
    print(f"Summarization failed: {e}")
    # Handle error appropriately
```

## Example 9: Processing Web Content

```python
import requests
from bedrock_summarizer import BedrockSummarizer

# Fetch article from web
response = requests.get('https://example.com/article')
text = response.text  # Or use BeautifulSoup to extract main content

# Summarize
summarizer = BedrockSummarizer()
summaries = summarizer.summarize_all_lengths(text)
print(summaries['medium'])
```

## Example 10: Integration with File Watcher

Monitor a folder and auto-summarize new files:

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bedrock_summarizer import BedrockSummarizer

class SummaryHandler(FileSystemEventHandler):
    def __init__(self):
        self.summarizer = BedrockSummarizer()
    
    def on_created(self, event):
        if event.src_path.endswith('.txt'):
            with open(event.src_path, 'r') as f:
                text = f.read()
            summary = self.summarizer.generate_summary(text, 'medium')
            print(f"New file summarized: {event.src_path}")
            print(summary)

observer = Observer()
observer.schedule(SummaryHandler(), path='.', recursive=False)
observer.start()
```

## Tips

1. **Optimal Text Length**: Works best with 100-5000 words
2. **Cost Optimization**: Use Haiku for most tasks, Sonnet for important content
3. **Rate Limits**: Bedrock has rate limits; add delays for batch processing
4. **Token Limits**: Very long texts may need chunking (not implemented in basic version)
5. **Language**: Works with multiple languages, but English gives best results
