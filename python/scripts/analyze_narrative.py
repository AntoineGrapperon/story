import argparse
import os
import json
import re
import ollama # Assuming ollama library is used for LLM interaction

# Define the output directory for narrative analysis reports
OUTPUT_DIR = "output/narrative_analysis_reports"

def read_text_file(file_path):
    """Reads the content of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Story file not found at {file_path}")
        return None

def identify_setups(story_text: str, ollama_model: str, max_context_words: int) -> list:
    """
    Identifies potential narrative setups within the story text using an LLM.
    Returns a list of dictionaries, each describing a setup.
    """
    print(f"Identifying setups using model: {ollama_model} for {len(story_text.split())} words, max context: {max_context_words}")
    
    # Chunk the story text to fit within LLM context window if necessary
    # For simplicity, initially, we'll send the whole text, but this might need chunking for long stories.
    # The current `max_context_words` argument for identify_setups is meant for the LLM's internal processing.

    prompt = f"""You are an expert narrative analyst. Your task is to identify potential "setups" in the provided story text.
A "setup" is a detail, character trait, object, skill, or event introduced into a story that seems insignificant at the time but *could* become crucial or relevant later. Focus on details that hint at future events, character development, or plot points.

Be inclusive: list anything that *might* be a setup, even if you are not certain. Do NOT try to find payoffs in this step.

Your response MUST be a JSON array of objects, where each object represents a setup with the following keys:
- "id": A unique identifier for the setup (e.g., "S1", "S2").
- "description": A brief, concise description of the setup.
- "location": A short quote or reference from the story where the setup is introduced.

If no potential setups are found, respond with an empty JSON array: [].

Story Text:
{story_text[:max_context_words * 5]} # Sending a truncated version if story is very long, max_context_words is just a guide for LLM.
(Note: The story text has been potentially truncated for brevity, focus on the available text.)

JSON Array of Setups:
"""
    
    try:
        response = ollama.generate(model=ollama_model, prompt=prompt)
        llm_output = response.get('response', '').strip()
        
        # Attempt to parse JSON output
        setups = json.loads(llm_output)
        if not isinstance(setups, list):
            print(f"Warning: LLM response for setups was not a JSON list as expected. Output: {llm_output}")
            return []
        
        # Basic validation for setup structure
        validated_setups = []
        for setup in setups:
            if all(k in setup for k in ["id", "description", "location"]):
                validated_setups.append(setup)
            else:
                print(f"Warning: Malformed setup object from LLM: {setup}")
        return validated_setups

    except ollama.ResponseError as e:
        print(f"Error communicating with Ollama server during setup identification: {e}")
        return []
    except json.JSONDecodeError:
        print(f"Error parsing JSON response from Ollama during setup identification. LLM output: {llm_output}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during setup identification Ollama interaction: {e}")
        return []

def analyze_payoffs(story_text: str, setups: list, ollama_model: str, max_context_words: int) -> list:
    """
    Analyzes identified setups to find their payoffs or mark them as unfulfilled.
    Returns a list of dictionaries, each describing a setup with its payoff status.
    """
    print(f"Analyzing payoffs for {len(setups)} setups using model: {ollama_model}, max context: {max_context_words}")
    
    analyzed_results = []
    for setup in setups:
        print(f"  - Analyzing setup '{setup['description']}' (ID: {setup['id']})...")
        prompt = f"""You are an expert narrative analyst. You have identified the following "setup" in a story:

Setup ID: {setup['id']}
Description: {setup['description']}
Introduced At: {setup['location']}

Now, review the ENTIRE provided story text again. Your task is to determine if this specific setup has a "payoff" or if it remains "unfulfilled."
A "payoff" is a later event, revelation, or consequence in the story where the setup becomes clearly relevant, crucial, or resolved.

Your response MUST be a JSON object with the following keys:
- "id": The ID of the setup (e.g., "S1").
- "status": "Paid Off" if a clear payoff is found, otherwise "Unfulfilled".
- "payoff_description": A brief description of the payoff if "Paid Off". If "Unfulfilled", state "No clear payoff found."
- "payoff_location": The approximate location (e.g., chapter/paragraph reference or short quote) of the payoff if "Paid Off". If "Unfulfilled", state "N/A".

Do NOT include any other text or conversational filler. Only provide the JSON object.

Story Text:
{story_text[:max_context_words * 5]} # Sending a truncated version if story is very long, max_context_words is just a guide for LLM.
(Note: The story text has been potentially truncated for brevity, focus on the available text.)

JSON Object:
"""
        try:
            response = ollama.generate(model=ollama_model, prompt=prompt)
            llm_output = response.get('response', '').strip()
            
            payoff_analysis = json.loads(llm_output)
            if not isinstance(payoff_analysis, dict) or not all(k in payoff_analysis for k in ["id", "status", "payoff_description", "payoff_location"]):
                print(f"Warning: LLM response for payoff analysis was not a valid JSON object or missing keys. Output: {llm_output}")
                # Default to unfulfilled if LLM response is malformed
                analyzed_results.append({
                    **setup,
                    "status": "Unfulfilled",
                    "payoff_description": "LLM response malformed or missing keys.",
                    "payoff_location": "N/A"
                })
                continue
            
            analyzed_results.append({**setup, **payoff_analysis})

        except ollama.ResponseError as e:
            print(f"Error communicating with Ollama server during payoff analysis for setup {setup['id']}: {e}")
            analyzed_results.append({
                **setup,
                "status": "Unfulfilled",
                "payoff_description": f"Error communicating with LLM: {e}",
                "payoff_location": "N/A"
            })
        except json.JSONDecodeError:
            print(f"Error parsing JSON response from Ollama during payoff analysis for setup {setup['id']}. LLM output: {llm_output}")
            analyzed_results.append({
                **setup,
                "status": "Unfulfilled",
                "payoff_description": f"Error parsing LLM JSON: {llm_output}",
                "payoff_location": "N/A"
            })
        except Exception as e:
            print(f"An unexpected error occurred during payoff analysis Ollama interaction for setup {setup['id']}: {e}")
            analyzed_results.append({
                **setup,
                "status": "Unfulfilled",
                "payoff_description": f"Unexpected error during LLM interaction: {e}",
                "payoff_location": "N/A"
            })
    return analyzed_results

def generate_report(story_filepath: str, analysis_results: list, output_dir: str):
    """
    Generates a markdown report of the narrative analysis.
    """
    story_title = os.path.splitext(os.path.basename(story_filepath))[0]
    output_filename = os.path.join(output_dir, f"{story_title}_narrative_analysis_report.md")
    
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Narrative Analysis Report: {story_title}\n\n")
        f.write("## Setups and Payoffs\n\n")
        
        unfulfilled_setups = []
        for result in analysis_results:
            f.write(f"### Setup ID: {result['id']}\n")
            f.write(f"- **Description:** {result['description']}\n")
            f.write(f"- **Introduced At:** {result['location']}\n")
            f.write(f"- **Status:** {result['status']}\n")
            if result['status'] == "Paid Off":
                f.write(f"- **Payoff Description:** {result['payoff_description']}\n")
                f.write(f"- **Payoff Location:** {result['payoff_location']}\n")
            else:
                unfulfilled_setups.append(result)
            f.write("\n")
        
        if unfulfilled_setups:
            f.write("## Unfulfilled Setups\n\n")
            for setup in unfulfilled_setups:
                f.write(f"### Setup ID: {setup['id']}\n")
                f.write(f"- **Description:** {setup['description']}\n")
                f.write(f"- **Introduced At:** {setup['location']}\n")
                f.write(f"- **Reason Unfulfilled:** {setup['payoff_description']} (LLM determined)\n")
                f.write("\n")

    print(f"Narrative analysis report saved to {output_filename}")


def main():
    parser = argparse.ArgumentParser(description="Perform a two-step LLM-based narrative analysis for setups and payoffs.")
    parser.add_argument("story_filepath", help="Path to the story text file for analysis.")
    parser.add_argument("--ollama_model", default="llama3.2:3b",
                        help="The Ollama model to use for both setup identification and payoff analysis.")
    parser.add_argument("--output_dir", default=OUTPUT_DIR,
                        help=f"Directory to save the narrative analysis report. Defaults to '{OUTPUT_DIR}'.")
    parser.add_argument("--max_context_words_setup", type=int, default=1000,
                        help="Maximum total number of words for the context sent to LLM during setup identification.")
    parser.add_argument("--max_context_words_payoff", type=int, default=1500,
                        help="Maximum total number of words for the context sent to LLM during payoff analysis (per setup).")
    args = parser.parse_args()

    # --- Step 0: Initial Setup and Validation ---
    story_text = read_text_file(args.story_filepath)
    if story_text is None:
        return

    # --- Step 1: Setup Identification ---
    print("
--- Step 1: Identifying Setups ---")
    setups = identify_setups(story_text, args.ollama_model, args.max_context_words_setup)
    if not setups:
        print("No setups identified. Aborting analysis.")
        return

    # --- Step 2: Payoff Analysis ---
    print("
--- Step 2: Analyzing Payoffs ---")
    analysis_results = analyze_payoffs(story_text, setups, args.ollama_model, args.max_context_words_payoff)
    
    # --- Step 3: Generate Report ---
    print("
--- Step 3: Generating Report ---")
    generate_report(args.story_filepath, analysis_results, args.output_dir)
    print("
Narrative analysis complete.")

if __name__ == "__main__":
    main()
