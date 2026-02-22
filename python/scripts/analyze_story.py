import argparse
import math
import re

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

if __name__ == "__main__":
    main()
