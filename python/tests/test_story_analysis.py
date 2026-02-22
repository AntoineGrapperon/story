import subprocess
import os
import pytest

# Define paths relative to the project root
ANALYSIS_SCRIPT = "python/scripts/analyze_story.py"
RAW_DATA_DIRECTORY = "data/raw_stories"

def test_story_analysis_suite(tmp_path):
    """
    Runs the story analysis script on raw data files and verifies output.
    """
    output_dir = tmp_path / "analysis_results"
    output_dir.mkdir()

    # Get all markdown files from the raw_data_dir
    # Note: This assumes the test is run from the project root or raw_data_dir is absolute
    raw_data_absolute_path = os.path.abspath(RAW_DATA_DIRECTORY)
    raw_story_files = [f for f in os.listdir(raw_data_absolute_path) if f.endswith('.md')]

    assert raw_story_files, "No raw story files found in the data directory."

    for story_file in raw_story_files:
        input_filepath = os.path.join(raw_data_absolute_path, story_file)
        # Create an output filename by changing the extension and adding a prefix
        output_filename = f"analysis_report_{os.path.splitext(story_file)[0]}.txt"
        output_filepath = output_dir / output_filename

        print(f"Running analysis for: {input_filepath}")
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
            print(f"Analysis successful for {story_file}.")
            
            # Assert that the output file was created and is not empty
            assert output_filepath.exists()
            assert output_filepath.stat().st_size > 0

        except subprocess.CalledProcessError as e:
            pytest.fail(f"Error running analysis for {story_file}:\nStdout: {e.stdout}\nStderr: {e.stderr}")
        except FileNotFoundError:
            pytest.fail(f"Error: Python interpreter or script not found. Check paths.")

