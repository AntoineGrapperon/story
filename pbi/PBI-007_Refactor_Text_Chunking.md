# PBI-007: Refactor Text Chunking Functionality

## Description
The `chunk_text` function, currently embedded within `python/scripts/analyze_narrative.py`, needs to be refactored into a reusable utility module. This will promote code reusability and maintainability, allowing other analysis scripts to leverage the same chunking logic.

Additionally, the chunking mechanism should be thoroughly reviewed to ensure it effectively splits text into meaningful segments based on sentence boundaries, rather than arbitrary line breaks or fixed character counts that might disrupt semantic meaning.

## Acceptance Criteria
- [x] A new Python module (e.g., `python/utils/text_chunking.py`) is created to house the `chunk_text` function and any related text processing utilities.
- [x] The `chunk_text` function is moved from `python/scripts/analyze_narrative.py` to the new utility module.
- [x] `python/scripts/analyze_narrative.py` is updated to import and use the `chunk_text` function from the new utility module.
- [x] The `chunk_text` function's logic is confirmed to primarily chunk text based on sentence boundaries, ensuring that sentences are not arbitrarily cut in half (unless a single sentence exceeds the maximum chunk size).
- [x] Unit tests are added or updated for the `chunk_text` function in its new location to verify its correct behavior, especially concerning sentence boundary detection and handling of various text inputs.
- [x] All existing analysis scripts that require text chunking are updated to use the new utility function. (Initial scope: `analyze_narrative.py`)

## Technical Notes
- Consider creating a `python/utils/` directory for this new module.
- The `re` module is likely to be useful for robust sentence splitting.
- The `chunk_text` function already uses `re.split(r'(?<=[.!?])\s+', text)`, which is a good start for sentence-based splitting. The review should ensure this is robust for all expected input variations.