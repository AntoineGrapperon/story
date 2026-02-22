
import re

def extract_chapter(input_filepath, output_filepath, chapter_number):
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

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.writelines(chapter_lines)

if __name__ == "__main__":
    input_file = "data/raw_stories/The_Three_Musketeers.md"
    output_file = "data/raw_stories/Chapter_1_The_Three_Musketeers.md"
    chapter_num = 1
    extract_chapter(input_file, output_file, chapter_num)
