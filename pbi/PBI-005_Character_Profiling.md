# PBI-005: Implement Character Profiling for Fiction Writing

## Goal
Generate a Markdown file for each prominent character in a story, summarizing their characteristics based on fiction writing principles.

## Description
This PBI focuses on creating a new Python script (`character_profiler.py`) that utilizes LLM capabilities to perform in-depth characterization.

### Phases:
1.  **Character Identification:** Identify a list of prominent characters from the story text (e.g., using existing `analyze_story.py` or a simplified manual/regex approach).
2.  **Characterization Data Extraction (LLM-Driven):** For each identified character:
    *   Extract relevant contextual text (sentences/paragraphs) from the full story where the character is mentioned.
    *   Prompt an LLM (Ollama) to summarize the character based on key fiction writing characterization elements (Physical Appearance, Personality Traits, Backstory, Motivations, Strengths/Weaknesses, Relationships, Dialogue, Actions, Internal Thoughts, Growth/Arc).
3.  **Markdown File Generation:** Create a structured Markdown file for each character, containing their LLM-generated profile.

## Acceptance Criteria
- A new script `python/scripts/character_profiler.py` is created.
- The script successfully identifies a configurable list of main characters.
- For each character, the script generates a Markdown file in `output/character_summaries/`.
- Each Markdown file contains a summary of the character, structured with headings corresponding to the key characterization elements.
- The character summaries are coherent and reflect information present in the story text.

## Dependencies
- Ollama server must be running and accessible with a suitable LLM (e.g., `llama2`, `llama3.2:3b`).
- Existing `python/scripts/analyze_story.py` (for potential character identification or text processing utilities).
