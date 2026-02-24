**PBI-006: Implement Two-Step Setup and Payoff Detection**

**Title:** Implement Two-Step LLM Process for Setup and Payoff Detection

**Description:**
As a story analyst,
I want to identify narrative setups and their corresponding payoffs (or lack thereof) within a story,
So that I can gain deeper insights into the narrative structure, pacing, and completeness of story arcs.

This PBI involves developing a two-step process using Large Language Models (LLMs) to systematically analyze a given story text. The process will first identify potential "setups" and then, in a second pass, determine their "payoffs" or identify them as "unfulfilled."

**Step 1: Setup Identification**
The LLM will perform an initial pass over the story text to identify and log all potential narrative "setups." A setup is defined as a detail, character trait, object, skill, or event that appears to be introduced early and *could* become significant later. The LLM should be inclusive in its identification and not attempt to find payoffs in this stage.

**Step 2: Payoff Analysis and Unfulfilled Setup Reporting**
Using the list of identified setups from Step 1, the LLM will perform a second pass over the story text. For each setup, it will search for a corresponding "payoff"—a later event or revelation where the setup becomes relevant. If a payoff is found, it will be described and linked to the setup. If no clear payoff is found after a thorough search, the setup will be explicitly marked as "unfulfilled."

**Acceptance Criteria:**

*   **AC1: Input Processing:** The system can accept a story text file as input for analysis.
*   **AC2: Setup Extraction (Step 1):** The system successfully executes an LLM-based process to generate a list of potential setups from the input story. Each identified setup must include:
    *   A unique identifier.
    *   A brief description of the setup.
    *   The approximate location (e.g., chapter/paragraph reference or short quote) where the setup was introduced.
*   **AC3: Payoff Analysis (Step 2):** The system successfully executes an LLM-based process that takes the story text and the list of setups from AC2, and for each setup:
    *   Identifies and describes a corresponding payoff within the story, including its approximate location, if one exists.
    *   Explicitly marks the setup as "Unfulfilled" if no clear payoff is identified.
*   **AC4: Comprehensive Report Generation:** The system generates a consolidated markdown report (or similar human-readable format) that includes:
    *   The original story title/metadata.
    *   A list of all identified setups and their associated payoffs.
    *   A dedicated section listing all setups that were identified as "Unfulfilled."
    *   Each entry in the report should clearly link the setup to its payoff/status and relevant locations.
*   **AC5: LLM Configuration:** The solution allows for configuration of the LLM model (e.g., Ollama model name) and any relevant parameters (e.g., chunk size, context word limits for each step).
*   **AC6: Error Handling:** The system gracefully handles cases where LLM communication fails or returns unparseable output during either step, providing informative error messages in the report.
*   **AC7: Performance (Non-functional):** While initial performance may vary depending on story length and LLM, the process should complete for a "small" test chapter (e.g., `test_chapter.md`) within a reasonable timeframe (e.g., under 5-10 minutes per full analysis run).