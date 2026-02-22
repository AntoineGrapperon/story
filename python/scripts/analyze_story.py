import argparse
import math
import re
import ollama
import json

def identify_characters_with_ollama(text, model="llama2"):
    """
    Identifies characters and their frequencies using a local Ollama server.
    Assumes Ollama server is running and the specified model is available.
    """
    prompt = f"""Given only the following story text, identify all named characters and their frequency.
Your response MUST be a JSON object with keys as character names and values as their frequencies.
Do NOT include any other text or conversational filler.
Only include actual character names found strictly within the provided story text, not generic terms or common nouns, and do not infer characters.
If no named characters are found in the provided story text, respond ONLY with the following JSON: {{"error": "No named characters found in the provided text."}}

Story Text:
{text}

JSON Response:
"""
    try:
        response = ollama.generate(model=model, prompt=prompt)
        # The Ollama response typically contains a 'response' field with the LLM's output.
        # We expect this output to be a JSON string.
        llm_output = response.get('response', '').strip()
        try:
            parsed_json = json.loads(llm_output)
            if isinstance(parsed_json, dict) and parsed_json.get("error") == "No named characters found in the provided text.":
                print("No named characters found in the provided text (as per LLM).")
                return {}
            elif isinstance(parsed_json, dict):
                return parsed_json
            else:
                print(f"Warning: LLM response was not a JSON object as expected.")
                return {}
        except json.JSONDecodeError:
            print(f"Error parsing JSON response from Ollama. LLM output: {llm_output}")
            return {}
    except ollama.ResponseError as e:
        print(f"Error communicating with Ollama server: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response from Ollama: {e}")
        print(f"LLM output: {llm_output}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred during Ollama interaction: {e}")
        return {}

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
    characters = identify_characters_with_ollama(text_content, model=args.ollama_model)
    if characters:
        for char, freq in characters.items():
            print(f"- {char}: {freq}")
    else:
        print("No characters identified or an error occurred.")

if __name__ == "__main__":
    main()
