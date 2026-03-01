import subprocess
import os
import pytest
import shutil

# Define paths relative to the project root
CHARACTER_PROFILER_SCRIPT = "story/profiler.py"
RAW_DATA_DIRECTORY = "data/raw_stories"
OUTPUT_CHARACTER_SUMMARIES_DIR = "output/character_summaries"

@pytest.fixture(autouse=True)
def cleanup_output_dir():
    """Fixture to clean up the output directory before and after tests."""
    # Ensure the output directory exists before tests run
    os.makedirs(OUTPUT_CHARACTER_SUMMARIES_DIR, exist_ok=True)
    
    # Clean up before test
    for file_name in os.listdir(OUTPUT_CHARACTER_SUMMARIES_DIR):
        file_path = os.path.join(OUTPUT_CHARACTER_SUMMARIES_DIR, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
            
    yield # Run the test
    
    # Clean up after test (optional, can be removed if you want to inspect outputs)
    for file_name in os.listdir(OUTPUT_CHARACTER_SUMMARIES_DIR):
        file_path = os.path.join(OUTPUT_CHARACTER_SUMMARIES_DIR, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def test_character_profiling_d_artagnan():
    """
    Tests the character profiler script for D'Artagnan from 'test_chapter.md'.
    """
    input_story_file = os.path.join(RAW_DATA_DIRECTORY, "test_chapter.md")
    character_name = "D'Artagnan"
    output_filename = f"{character_name.replace(' ', '_')}.md"
    output_filepath = os.path.join(OUTPUT_CHARACTER_SUMMARIES_DIR, output_filename)

    print(f"Running character profiler for: {character_name} from {input_story_file}")
    print(f"Expected output to: {output_filepath}")

    # Create a environment that includes our mock ollama
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("tests/mocks") + os.pathsep + env.get("PYTHONPATH", "")

    try:
        # Run the character profiler script as a subprocess
        result = subprocess.run(
            ["python", CHARACTER_PROFILER_SCRIPT, input_story_file, character_name, "--ollama_model", "llama3.2:3b"],
            capture_output=True,
            text=True,
            check=True,  # Raise an exception for non-zero exit codes
            env=env
        )
        print(f"Script stdout:\n{result.stdout}")
        if result.stderr:
            print(f"Script stderr:\n{result.stderr}")
        
        # Assert that the output file was created and is not empty
        assert os.path.exists(output_filepath)
        assert os.path.getsize(output_filepath) > 0

        # Read the content of the generated summary
        with open(output_filepath, 'r', encoding='utf-8') as f:
            summary_content = f.read()
        
        # Basic check for content - ensure character name is in the summary
        assert character_name in summary_content
        assert "### Physical Appearance" in summary_content
        assert "### Personality Traits" in summary_content
        assert "### Motivations & Goals" in summary_content

    except subprocess.CalledProcessError as e:
        pytest.fail(f"""Error running character profiler for {character_name}:
Stdout: {e.stdout}
Stderr: {e.stderr}""")
    except FileNotFoundError:
        pytest.fail(f"Error: Python interpreter or script not found. Check paths.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
