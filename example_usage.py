"""
Example: Using BedrockSummarizer as a module in your own code
"""

from bedrock_summarizer import BedrockSummarizer

# Sample text to summarize
article = """
The Internet of Things (IoT) is revolutionizing how we interact with the physical world. 
By connecting everyday devices to the internet, IoT enables unprecedented levels of automation, 
monitoring, and control. Smart homes can adjust temperature and lighting based on occupancy. 
Industrial sensors monitor equipment health and predict maintenance needs. Wearable devices 
track health metrics and alert users to potential issues. Cities are becoming smarter with 
connected traffic lights, parking systems, and waste management. However, IoT also presents 
challenges including security vulnerabilities, privacy concerns, and the need for standardization 
across different platforms and manufacturers.
"""

def main():
    """Example usage of BedrockSummarizer."""
    
    # Initialize the summarizer
    summarizer = BedrockSummarizer(region='us-east-1')
    
    print("Example 1: Generate all three summary lengths")
    print("=" * 60)
    
    try:
        summaries = summarizer.summarize_all_lengths(article)
        
        print("\nShort Summary:")
        print(summaries['short'])
        
        print("\n\nMedium Summary:")
        print(summaries['medium'])
        
        print("\n\nLong Summary:")
        print(summaries['long'])
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("\nExample 2: Generate only a specific length")
    print("=" * 60)
    
    try:
        short_summary = summarizer.generate_summary(article, 'short')
        print("\nShort Summary Only:")
        print(short_summary)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
