import argparse
import os
import re
import ollama
import json

# Define the output directory for character summaries
OUTPUT_DIR = "output/character_summaries"

def read_text_file(file_path):
    """Reads the content of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Story file not found at {file_path}")
        return None

def extract_character_context(story_text, character_name, lines_around_mention=5, max_total_context_words=1000):
    """
    Extracts sentences/paragraphs around mentions of the character,
    limiting the total context length.
    """
    context_lines_with_indices = [] # Store (index, line) to maintain order later
    lines = story_text.split('\n')
    
    # Pre-compile regex for efficiency
    char_regex = re.compile(r'\b' + re.escape(character_name) + r'\b', re.IGNORECASE)

    for i, line in enumerate(lines):
        if char_regex.search(line):
            # Add lines around the mention
            start_index = max(0, i - lines_around_mention)
            end_index = min(len(lines), i + lines_around_mention + 1)
            for j in range(start_index, end_index):
                stripped_line = lines[j].strip()
                if stripped_line: # Only add non-empty lines
                    context_lines_with_indices.append((j, stripped_line))

    # Remove duplicates and sort by original line number
    unique_context_lines = []
    seen_lines = set()
    for index, line in sorted(context_lines_with_indices, key=lambda x: x[0]):
        if line not in seen_lines:
            unique_context_lines.append(line)
            seen_lines.add(line)

    full_context = "\n".join(unique_context_lines)

    # Truncate by words if too long
    words = full_context.split()
    if len(words) > max_total_context_words:
        full_context = " ".join(words[:max_total_context_words]) + "..."
    
    return full_context

def generate_character_summary(character_name, character_context, llm_model="llama2"):
    """
    Generates a character summary using Ollama based on the provided context.
    """
    if not character_context:
        return f"No significant context found for {character_name} to generate a summary."

    prompt = f"""Based *only* on the following text excerpts from a story, create a detailed characterization for "{character_name}" following these fiction writing elements. Your response must be in Markdown format, with each element as a separate heading.

Character Name: {character_name}

## Physical Appearance:
(Describe how they look. If not mentioned, state 'Not explicitly described.')

## Personality Traits:
(Describe their typical behavior, attitudes, and temperament. Use adjectives and provide brief examples if the text allows.)

## Backstory/History:
(Mention relevant past events or upbringing that shaped them, if described.)

## Motivations & Goals:
(What drives them? What do they want to achieve, based on their actions and thoughts in the text?)

## Strengths & Weaknesses:
(Identify their admirable qualities, skills, and flaws/vulnerabilities.)

## Relationships:
(How do they interact with other characters mentioned in the text? Provide specific names if possible.)

## Dialogue & Speech Patterns:
(Describe their unique way of speaking, if distinct. Provide a short example if available.)

## Actions & Behavior:
(Summarize their key actions and choices in the provided text.)

## Internal Thoughts & Feelings:
(What inner thoughts or emotions are revealed? If not directly revealed, infer from actions.)

## Growth & Arc (Initial Impression):
(How do they change or develop in the provided excerpts, or what is their initial trajectory? If no change, describe their static state.)

---
Story Excerpts for {character_name}:
{character_context}
---

Your Characterization:
"""
    print(f"Sending prompt for {character_name} to Ollama...")
    try:
        response = ollama.generate(model=llm_model, prompt=prompt)
        llm_output = response.get('response', '').strip()
        return llm_output
    except ollama.ResponseError as e:
        return f"Error communicating with Ollama server for {character_name}: {e}"
    except Exception as e:
        return f"An unexpected error occurred during Ollama interaction for {character_name}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Generate character profiles from a story using Ollama.")
    parser.add_argument("story_filepath", help="Path to the story text file.")
    parser.add_argument("character_name", help="Name of the character to profile.")
    parser.add_argument("--ollama_model", default="llama2",
                        help="The Ollama model to use for characterization (e.g., llama2, mistral).")
    # Add arguments for context control
    parser.add_argument("--lines_around_mention", type=int, default=5,
                        help="Number of lines to extract around each character mention.")
    parser.add_argument("--max_total_context_words", type=int, default=1000,
                        help="Maximum total number of words for the context sent to LLM.")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    story_text = read_text_file(args.story_filepath)
    if story_text is None:
        return

    print(f"Profiling character: {args.character_name}")
    character_context = extract_character_context(
        story_text,
        args.character_name,
        lines_around_mention=args.lines_around_mention,
        max_total_context_words=args.max_total_context_words
    )
    
    # Call Ollama for character summary
    character_summary = generate_character_summary(args.character_name, character_context, args.ollama_model)

    output_filename = os.path.join(OUTPUT_DIR, f"{args.character_name.replace(' ', '_')}.md")
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(character_summary)
    print(f"Character profile for {args.character_name} saved to {output_filename}")

if __name__ == "__main__":
    main()
