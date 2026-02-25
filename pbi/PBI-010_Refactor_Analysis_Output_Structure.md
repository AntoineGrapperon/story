# PBI-010: Refactor Analysis Scripts for Decoupled Output Structure

## Description
Currently, the output structure of analysis scripts (e.g., narrative analysis) might be heavily reliant on the LLM's direct response format. This PBI aims to refactor these scripts to introduce a clear separation between the LLM's raw output and the final structured report generation. The refactoring should allow for flexible output formats, specifically supporting JSON and Markdown, independent of the LLM's internal output format.

## Acceptance Criteria
- [ ] Analysis scripts (starting with `analyze_narrative.py`) are refactored to process raw LLM output into an intermediary, standardized data structure (e.g., Python dictionaries or objects) before final report generation.
- [ ] A mechanism is implemented within the analysis scripts (or a new utility module) to generate reports in either JSON or Markdown format based on the standardized intermediary data structure.
- [ ] A command-line argument (e.g., `--output_format json` or `--output_format markdown`) is added to relevant analysis scripts to allow users to specify the desired output format.
- [ ] When `json` format is selected, the script outputs a well-formed JSON file containing all analysis results.
- [ ] When `markdown` format is selected, the script outputs a human-readable Markdown file, similar to the current reports.
- [ ] The LLM is primarily responsible for content generation (e.g., identifying setups, describing payoffs), while the script is responsible for structuring and formatting this content into the desired output format.
- [ ] Existing tests are updated, or new tests are added, to verify the correct generation of both JSON and Markdown output formats.

## Technical Notes
- Consider creating a `python/reporting/` directory for modules responsible for generating different report formats from a common data structure.
- The intermediary data structure should be robust enough to hold all information relevant to the analysis (e.g., setup IDs, descriptions, locations, status, payoff details).
- For Markdown generation, existing templates or string formatting can be adapted. For JSON, `json.dumps` will be used.
- Ensure backwards compatibility or clear migration paths for any existing consumers of the analysis script outputs.