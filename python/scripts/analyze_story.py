import argparse
import math
import re
import ollama
import json

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

def identify_characters_with_ollama(text_chunks, model="llama2"):
    """
    Identifies characters and their frequencies using a local Ollama server by processing text in chunks.
    Assumes Ollama server is running and the specified model is available.
    """
    aggregated_characters = {}

    for i, chunk in enumerate(text_chunks):
        print(f"Processing chunk {i+1}/{len(text_chunks)}...")
        prompt = f"""Given only the following story text, identify all named characters and their frequency.
Your response MUST be a JSON object with keys as character names and values as their frequencies.
Do NOT include any other text or conversational filler.
Only include actual character names found strictly within the provided story text, not generic terms or common nouns, and do not infer characters.
If no named characters are found in the provided story text, respond ONLY with the following JSON: {{"error": "No named characters found in the provided text."}}

Story Text:
{chunk}

JSON Response:
"""
        try:
            response = ollama.generate(model=model, prompt=prompt)
            llm_output = response.get('response', '').strip()
            
            parsed_json = json.loads(llm_output)
            if isinstance(parsed_json, dict) and parsed_json.get("error") == "No named characters found in the provided text.":
                print(f"No named characters found in chunk {i+1} (as per LLM).")
            elif isinstance(parsed_json, dict):
                for char, freq in parsed_json.items():
                    if char in aggregated_characters:
                        aggregated_characters[char] += freq
                    else:
                        aggregated_characters[char] = freq
            else:
                print(f"Warning: LLM response for chunk {i+1} was not a JSON object as expected. Output: {llm_output}")
        except ollama.ResponseError as e:
            print(f"Error communicating with Ollama server for chunk {i+1}: {e}")
        except json.JSONDecodeError:
            print(f"Error parsing JSON response from Ollama for chunk {i+1}. LLM output: {llm_output}")
        except Exception as e:
            print(f"An unexpected error occurred during Ollama interaction for chunk {i+1}: {e}")

    return aggregated_characters

def read_text_file(file_path):
    """
    Reads the content of a text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def calculate_word_count(text):
    """
    Calculates the number of words in a given text.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)

def estimate_reading_time(word_count, words_per_minute=200):
    """
    Estimates the reading time in minutes for a given word count.
    """
    if word_count == 0:
        return 0
    return math.ceil(word_count / words_per_minute)

def main():
    parser = argparse.ArgumentParser(description="Analyze a story text file.")
    parser.add_argument("file_path", help="Path to the story text file.")
    parser.add_argument("--ollama_model", default="llama2",
                        help="The Ollama model to use for character identification (e.g., llama2, mistral).")
    args = parser.parse_args()

    text_content = read_text_file(args.file_path)

    if text_content is None:
        print(f"Error: File not found at {args.file_path}")
        return

    word_count = calculate_word_count(text_content)
    reading_time = estimate_reading_time(word_count)

    print(f"--- Analysis Report for {args.file_path} ---")
    print(f"Word Count: {word_count}")
    print(f"Estimated Reading Time: {reading_time} minutes")

    print("\n--- Character Identification (via Ollama) ---")
    text_chunks = chunk_text(text_content)
    characters = identify_characters_with_ollama(text_chunks, model=args.ollama_model)
    if characters:
        for char, freq in characters.items():
            print(f"- {char}: {freq}")
    else:
        print("No characters identified or an error occurred.")

if __name__ == "__main__":
    main()
