import pytest
from story.utils.text_compression import compress_text

def test_compress_text_empty_string():
    assert compress_text("") == ""

def test_compress_text_removes_extra_whitespace():
    text = """  Hello   world! 
 This	is a test.  """
    compressed = compress_text(text)
    assert compressed == "Hello world! test."

def test_compress_text_removes_stopwords():
    text = "This is a test of the compression utility. And it works."
    compressed = compress_text(text)
    assert compressed == "test compression utility. works."

def test_compress_text_preserves_meaning_basic():
    text = "The quick brown fox jumps over the lazy dog."
    compressed = compress_text(text)
    assert compressed == "quick brown fox jumps lazy dog."

def test_compress_text_with_punctuation():
    text = "Hello, world! How are you?"
    compressed = compress_text(text)
    assert compressed == "Hello, world! you?"

def test_compress_text_case_insensitivity_stopwords():
    text = "A quick test. And THE result."
    compressed = compress_text(text)
    assert compressed == "quick test. result."

def test_compress_text_llm_method():
    # Note: This test assumes ollama is mocked via PYTHONPATH or other means
    text = "This is a longer sentence that needs to be summarized. It has several parts."
    compressed = compress_text(text, method="llm")
    # The mock returns this specific string
    assert compressed == "This is a mock LLM summary of the text."

def test_compress_text_llm_method_with_model():
    text = "Some text to compress."
    compressed = compress_text(text, method="llm", model="mistral")
    assert compressed == "This is a mock LLM summary of the text."

def test_compress_text_unknown_method_raises_error():
    with pytest.raises(ValueError, match="Unknown compression method: invalid_method"):
        compress_text("some text", method="invalid_method")

def test_llm_compress_text_empty_string():
    assert compress_text("", method="llm") == ""

def test_llm_compress_text_with_max_length():
    text = "This is a long piece of text that should be summarized."
    compressed = compress_text(text, method="llm", max_length=50)
    assert compressed == "This is a mock LLM summary of the text."
