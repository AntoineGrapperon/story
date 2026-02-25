import subprocess
import os
import pytest
import shutil

# Define paths relative to the project root
ANALYZE_NARRATIVE_SCRIPT = "story/scripts/analyze_narrative.py"
RAW_DATA_DIRECTORY = "data/raw_stories"
OUTPUT_NARRATIVE_REPORTS_DIR = "output/narrative_analysis_reports"

@pytest.fixture(autouse=True)
def cleanup_output_dir():
    """Fixture to clean up the output directory before and after tests."""
    # Ensure the output directory exists before tests run
    os.makedirs(OUTPUT_NARRATIVE_REPORTS_DIR, exist_ok=True)
    
    # Clean up before test
    for file_name in os.listdir(OUTPUT_NARRATIVE_REPORTS_DIR):
        file_path = os.path.join(OUTPUT_NARRATIVE_REPORTS_DIR, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
            
    yield # Run the test
    
    # Clean up after test (optional, can be removed if you want to inspect outputs)
    for file_name in os.listdir(OUTPUT_NARRATIVE_REPORTS_DIR):
        file_path = os.path.join(OUTPUT_NARRATIVE_REPORTS_DIR, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def test_narrative_analysis_test_chapter():
    """
    Tests the full narrative analysis script on 'test_chapter.md'.
    """
    input_story_file = os.path.join(RAW_DATA_DIRECTORY, "test_chapter.md")
    story_title = os.path.splitext(os.path.basename(input_story_file))[0]
    output_filename = f"{story_title}_narrative_analysis_report.md"
    output_filepath = os.path.join(OUTPUT_NARRATIVE_REPORTS_DIR, output_filename)

    print(f"Running narrative analysis for: {input_story_file}")
    print(f"Expected output report to: {output_filepath}")

    try:
        # Run the narrative analysis script as a subprocess
        result = subprocess.run(
            ["python", ANALYZE_NARRATIVE_SCRIPT, input_story_file, "--ollama_model", "llama3.2:3b", "--max_context_words_setup", "500", "--max_context_words_payoff", "1000"],
            capture_output=True,
            text=True,
            check=True,  # Raise an exception for non-zero exit codes
            timeout=600 # 10 minutes timeout for the full analysis
        )
        print(f"""Script stdout:
{result.stdout}""")
        if result.stderr:
            print(f"""Script stderr:
{result.stderr}""")
        
        # Assert that the output file was created and is not empty
        assert os.path.exists(output_filepath)
        assert os.path.getsize(output_filepath) > 0

        # Read the content of the generated report
        with open(output_filepath, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Basic checks for report content based on PBI AC4
        assert f"# Narrative Analysis Report: {story_title}" in report_content
        assert "## Setups and Payoffs" in report_content
        assert "### Setup ID:" in report_content # At least one setup should be reported
        assert "Status:" in report_content
        # It's hard to predict exact LLM output for payoff descriptions, but we can check for sections.
        # assert "## Unfulfilled Setups" in report_content # This might not always be present

    except subprocess.CalledProcessError as e:
        pytest.fail(f"""Error running narrative analysis for {input_story_file}:
Stdout: {e.stdout}
Stderr: {e.stderr}""")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Narrative analysis for {input_story_file} timed out after 10 minutes.")
    except FileNotFoundError:
        pytest.fail(f"Error: Python interpreter or script not found. Check paths.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
