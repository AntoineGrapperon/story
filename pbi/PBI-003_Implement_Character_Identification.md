# PBI-003: Implement Character Identification

## Goal
Add a heuristic-based character identification feature to `analyze_story.py`.

## Description
This item involves developing a preliminary method to identify potential character names within the text.
- Implement logic to scan the text for capitalized words that are not at the beginning of a sentence, or capitalized words that appear frequently.
- Filter out common words (e.g., "The", "And", "But") and other non-name entities.
- Count the frequency of each identified potential character name.

## Acceptance Criteria
- The script identifies a list of potential character names from the input text.
- Each identified character name is associated with its frequency in the text.
- The identification process shows reasonable accuracy in distinguishing names from common words (initial heuristic level).
