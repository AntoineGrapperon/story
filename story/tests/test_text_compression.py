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
    assert compressed == "Hello, world! How you?"

def test_compress_text_case_insensitivity_stopwords():
    text = "A quick test. And THE result."
    compressed = compress_text(text)
    assert compressed == "quick test. result."