import re

def chunk_text(text, chunk_size=1000):
    """
    Splits the given text into chunks of approximately `chunk_size` words,
    attempting to maintain sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk_words = []
    current_chunk_length = 0

    for sentence in sentences:
        sentence_words = sentence.split()
        sentence_length = len(sentence_words)

        # If adding the next sentence exceeds the chunk_size, start a new chunk
        # unless the current chunk is empty or the sentence itself is larger than chunk_size
        if current_chunk_length + sentence_length > chunk_size and current_chunk_words:
            chunks.append(" ".join(current_chunk_words))
            current_chunk_words = []
            current_chunk_length = 0

        current_chunk_words.extend(sentence_words)
        current_chunk_length += sentence_length
    
    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))
    
    return chunks