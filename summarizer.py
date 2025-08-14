from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sample text to summarize
text = """
Artificial General Intelligence (AGI) is the representation of generalized human cognitive abilities in software so that,
faced with an unfamiliar task, the AGI system could find a solution. AGI can theoretically perform any task that a human
being is capable of. It is a primary goal of some artificial intelligence research and a common topic in science fiction.
"""

# Generate summary
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)

print("Original text:\n", text)
print("\nSummary:\n", summary[0]['summary_text'])
