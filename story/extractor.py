import re
import argparse
import os

def extract_chapter(input_filepath, output_filepath, chapter_number):
    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found at {input_filepath}")
        return

    with open(input_filepath, 'r', encoding='utf-8') as f:
        content = f.readlines()

    chapter_start_pattern = re.compile(rf"^## {chapter_number} ")
    next_chapter_start_pattern = re.compile(rf"^## {chapter_number + 1} ")

    chapter_lines = []
    in_chapter = False

    for line in content:
        if chapter_start_pattern.match(line):
            in_chapter = True
        elif next_chapter_start_pattern.match(line) and in_chapter:
            break
        
        if in_chapter:
            chapter_lines.append(line)

    if not chapter_lines:
        print(f"Warning: No content found for chapter {chapter_number}.")
        return

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.writelines(chapter_lines)
    print(f"Chapter {chapter_number} extracted to {output_filepath}")

def main():
    parser = argparse.ArgumentParser(description="Extract a chapter from a story markdown file.")
    parser.add_argument("input_file", help="Path to the input story markdown file.")
    parser.add_argument("output_file", help="Path to the output markdown file.")
    parser.add_argument("chapter_number", type=int, help="The chapter number to extract.")
    
    args = parser.parse_args()
    extract_chapter(args.input_file, args.output_file, args.chapter_number)

if __name__ == "__main__":
    main()
