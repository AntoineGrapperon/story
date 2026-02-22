
# PBI-002: Implement Basic Text Analysis

## Goal
Add functionality to `analyze_story.py` to read a text file and calculate basic statistics.

## Description
This item focuses on the initial text processing capabilities of the script.
- Modify `python/scripts/analyze_story.py` to accept a file path as a command-line argument.
- Read the content of the specified text file.
- Calculate the total word count of the text.
- Estimate the reading time based on an average reading speed (e.g., 200 words per minute).

## Acceptance Criteria
- `analyze_story.py` can successfully read content from a given text file.
- The script correctly calculates and outputs the word count.
- The script correctly calculates and outputs the estimated reading time.

---

## Update: Chunking Verification

The `chunk_text` function within `analyze_story.py` has been verified to correctly split text into manageable chunks. This functionality is a prerequisite for character identification using large language models.

**Note:** The full `analyze_story.py` script, particularly the character identification feature, relies on a running Ollama server with the specified model (e.g., `llama3.2:3b`) available. Execution of the full example (`run_example_analysis.py`) may time out if the Ollama server is not properly configured or if model download/processing is lengthy.
