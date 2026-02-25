# PBI-008: Implement Text and Prompt Compression Utility

## Description
To optimize LLM interactions, especially with larger contexts or when dealing with token limits, a utility to compress text and prompts needs to be implemented. This utility should aim to reduce the token count of input text while preserving its core meaning and relevance for downstream analysis or LLM processing. This could involve various techniques such as summarization, keyword extraction, or more advanced methods.

## Acceptance Criteria
- [ ] A new Python module (e.g., `python/utils/text_compression.py`) is created to house text and prompt compression functionalities.
- [ ] The module provides at least one function (e.g., `compress_text(text: str) -> str`) that takes a string as input and returns a compressed version.
- [ ] The compression method demonstrably reduces the token count of typical input texts (e.g., story chunks, prompts).
- [ ] The compressed output retains the essential information and meaning of the original text to a reasonable degree, without introducing significant distortion or loss of critical details.
- [ ] Unit tests are added for the compression utility to verify its functionality, including token reduction and semantic preservation (where quantifiable).
- [ ] Documentation is provided for how to use the compression utility and its intended use cases.

## Technical Notes
- Consider different compression strategies, such as:
    - Extractive summarization (e.g., using LLMs, textrank, or other algorithms).
    - Keyword/keyphrase extraction.
    - Removing stop words or less critical descriptive language.
- The utility should be designed to be flexible, potentially allowing for different compression algorithms or parameters to be easily swapped or configured.
- Integration with an LLM for summarization might be an option, but a non-LLM based approach should also be considered for efficiency.