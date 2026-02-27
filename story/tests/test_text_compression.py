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

def test_compress_text_llm_method_placeholder():
    text = "This is a longer sentence that needs to be summarized. It has several parts. The goal is to see if the placeholder summarization works correctly by truncating the text."
    compressed = compress_text(text, method="llm", max_length=50)
    # The placeholder LLM summarization truncates by sentences or characters
    _max_length = 50 # Define max_length locally for the test
    expected_output = text[:_max_length]
    assert compressed == expected_output

def test_compress_text_llm_method_with_mock_llm_client():
    class MockLLMClient:
        def summarize(self, text_to_summarize, max_tokens):
            return f"LLM Summary of: {text_to_summarize[:max_tokens]}"

    mock_client = MockLLMClient()
    text = "This is a very long text that an LLM would summarize."
    compressed = compress_text(text, method="llm", llm_client=mock_client, max_length=20)
    assert compressed == "LLM Summary of: This is a very long ..."

def test_compress_text_unknown_method_raises_error():
    with pytest.raises(ValueError, match="Unknown compression method: invalid_method"):
        compress_text("some text", method="invalid_method")

def test_llm_compress_text_empty_string():
    assert compress_text("", method="llm") == ""

def test_llm_compress_text_no_llm_client_truncates():
    text = "This is a sentence. This is another sentence. This is a third sentence."
    compressed = compress_text(text, method="llm", max_length=20)
    assert compressed == "This is a sentence."

def test_llm_compress_text_with_llm_client():
    class MockLLMClient:
        def summarize(self, text_to_summarize, max_tokens):
            return f"Mocked LLM summary of: {text_to_summarize[:max_tokens]}..."
    
    mock_client = MockLLMClient()
    text = "This is a long piece of text that should be summarized by the mock LLM client."
    compressed = compress_text(text, method="llm", llm_client=mock_client, max_length=30)
    assert compressed == "LLM Summary of: This is a long piece of text t..."