import subprocess
import os
import shutil

# Define paths relative to the project root
ANALYSIS_SCRIPT = "python/scripts/analyze_story.py"
RAW_DATA_DIRECTORY = "data/raw_stories"
EXAMPLE_OUTPUT_DIRECTORY = "output/example_analysis_results"

def run_example_analysis():
    # Ensure the example output directory exists and is clean
    if os.path.exists(EXAMPLE_OUTPUT_DIRECTORY):
        shutil.rmtree(EXAMPLE_OUTPUT_DIRECTORY)
    os.makedirs(EXAMPLE_OUTPUT_DIRECTORY, exist_ok=True)

    # Get all markdown files from the raw_data_dir
    raw_data_absolute_path = os.path.abspath(RAW_DATA_DIRECTORY)
    raw_story_files = [f for f in os.listdir(raw_data_absolute_path) if f.endswith('.md')]

    if not raw_story_files:
        print(f"No raw story files found in {RAW_DATA_DIRECTORY} to analyze.")
        return

    print(f"--- Running Example Analysis ---")
    for story_file in raw_story_files:
        input_filepath = os.path.join(raw_data_absolute_path, story_file)
        output_filename = f"analysis_report_{os.path.splitext(story_file)[0]}.txt"
        output_filepath = os.path.join(EXAMPLE_OUTPUT_DIRECTORY, output_filename)

        print(f"
Analyzing: {input_filepath}")
        print(f"Saving report to: {output_filepath}")

        try:
            # Run the analysis script as a subprocess
            result = subprocess.run(
                ["python", ANALYSIS_SCRIPT, input_filepath],
                capture_output=True,
                text=True,
                check=True  # Raise an exception for non-zero exit codes
            )
            
            # Write the captured stdout to the output file
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"Analysis successful. Report saved.")

        except subprocess.CalledProcessError as e:
            print(f"Error running analysis for {story_file}:")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        except FileNotFoundError:
            print(f"Error: Python interpreter or script '{ANALYSIS_SCRIPT}' not found. Check paths.")
    print(f"
--- Example Analysis Complete. Reports in {EXAMPLE_OUTPUT_DIRECTORY} ---")

if __name__ == "__main__":
    run_example_analysis()
