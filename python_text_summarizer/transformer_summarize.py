#!/bin/python
from pathlib import Path
from transformers import pipeline
import sys

# Load a summarization pipeline
summarizer = pipeline("summarization")

# Text to summarize
try:
    filename = sys.argv[1]
    print("Using specified argument:", filename)
except IndexError:
    filename = 'summarize.txt'

print("Summarizing file:", filename)

text = Path(filename).read_text()

#text = """Text summarization is the process of reducing a text document in size while retaining key information.
#It is widely used in applications like search engines, news aggregation, and content recommendation."""

# Generate summary
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
print("Summary:", summary[0]['summary_text'])
