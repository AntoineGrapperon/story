import re
import ollama
from typing import Literal, Optional

def llm_compress_text(text: str, model: str = "llama3.2:3b", max_length: Optional[int] = None) -> str:
    """
    Compresses text using an LLM-based summarization approach via Ollama.

    Args:
        text (str): The input text to compress.
        model (str): The name of the Ollama model to use.
        max_length (Optional[int]): Optional hint for the maximum length of the summarized text.

    Returns:
        str: The LLM-compressed version of the text.
    """
    if not text:
        return ""

    prompt = f"Summarize the following text while preserving its core meaning and key details. Keep it concise.\n\nText:\n{text}\n\nSummary:"
    if max_length:
        prompt = f"Summarize the following text in approximately {max_length} characters or less, while preserving its core meaning and key details. Keep it concise.\n\nText:\n{text}\n\nSummary:"

    try:
        response = ollama.generate(model=model, prompt=prompt)
        return response.get('response', '').strip()
    except Exception as e:
        print(f"Error communicating with Ollama for text compression: {e}")
        # Fallback: return original text truncated to max_length if provided
        return text[:max_length] if max_length else text


def compress_text(text: str, method: Literal["simple", "llm"] = "simple", **kwargs) -> str:
    """
    Compresses text using a specified method.

    Args:
        text (str): The input text to compress.
        method (Literal["simple", "llm"]): The compression method to use.
                                            "simple" uses whitespace and stopword removal.
                                            "llm" uses an LLM-based summarization via Ollama.
        **kwargs: Additional arguments for the compression method (e.g., model, max_length for "llm" method).

    Returns:
        str: The compressed version of the text.
    """
    if method == "simple":
        if not text:
            return ""

        # Remove multiple spaces, tabs, newlines with a single space
        compressed_text = re.sub(r'\s+', ' ', text).strip()

        # Simple stopword removal (example set, can be expanded)
        stopwords = set([
            "a", "an", "the", "is", "am", "are", "was", "were", "be", "been", "being",
            "of", "in", "on", "at", "by", "for", "with", "from", "to", "and", "or", "but",
            "I", "he", "she", "it", "we", "you", "they", "me", "him", "her", "us", "them",
            "my", "your", "his", "her", "its", "our", "their",
            "this", "that", "those", "these", "over", "under", "through", "down", "up",
            "out", "in", "on", "off", "as", "at", "by", "for", "with", "about", "against",
            "between", "into", "through", "during", "before", "after", "above", "below",
            "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how",
            "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
            "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
            "s", "t", "can", "will", "just", "don", "should", "now"
        ])
        words = compressed_text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        
        return " ".join(filtered_words)
    elif method == "llm":
        return llm_compress_text(text, **kwargs)
    else:
        raise ValueError(f"Unknown compression method: {method}")

# Future implementations could include:
# - Keyword extraction
# - More advanced text reduction algorithms
