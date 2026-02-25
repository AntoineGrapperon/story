import pytest
from story.utils.text_chunking import chunk_text

def test_chunk_text_basic():
    text = "This is the first sentence. This is the second sentence. And here is the third one."
    chunks = chunk_text(text, chunk_size=10)
    assert len(chunks) >= 1
    assert all(len(chunk.split()) <= 10 for chunk in chunks)
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "") # Ensure all text is present

def test_chunk_text_empty_string():
    text = ""
    chunks = chunk_text(text, chunk_size=10)
    assert chunks == []

def test_chunk_text_single_sentence_exceeds_chunk_size_no_split():
    text = "This is a very long single sentence that should still be chunked correctly even if the chunk size is small."
    chunks = chunk_text(text, chunk_size=5)
    assert len(chunks) == 1 # Expecting only one chunk for a single long sentence
    assert len(chunks[0].split()) > 5 # The single chunk should exceed the chunk_size
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "") # Ensure all text is present

def test_chunk_text_preserves_sentence_boundaries():
    text = "Sentence one. Sentence two? Sentence three! Final sentence."
    chunks = chunk_text(text, chunk_size=3) # Force chunks to be small
    # Expecting chunks to mostly respect sentence boundaries,
    # though small chunk_size can break single long sentences.
    # We primarily check that the split points are reasonable.
    assert "Sentence one." in chunks[0] or "Sentence one. Sentence two?" in chunks[0]
    assert "Final sentence." in chunks[-1]

def test_chunk_text_with_various_punctuation():
    text = "Hello world. How are you? I am fine! Really. Very good."
    chunks = chunk_text(text, chunk_size=5)
    assert len(chunks) >= 1
    assert "Hello world." in chunks[0]
    assert "How are you?" in chunks[0] or "How are you?" in chunks[1] # Depending on chunk_size
    assert "Very good." in chunks[-1]

def test_chunk_text_long_words():
    text = "Antidisestablishmentarianism is a very long word. Another longword."
    chunks = chunk_text(text, chunk_size=2) # Very small chunk size
    assert len(chunks) > 1
    assert "Antidisestablishmentarianism" in chunks[0] or "Antidisestablishmentarianism" in chunks[1]
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "")