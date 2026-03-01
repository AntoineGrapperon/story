# PBI-011: Implement Streamlit Web Interface

## Description
Develop a web-based user interface using Streamlit to provide an interactive and accessible way for users to perform story analysis. The interface will allow users to upload text files, trigger the analysis process, visualize results, and download reports. This PBI also covers the architectural decision to use Streamlit for its rapid prototyping capabilities and extensibility for future features like user management.

## Acceptance Criteria
- [ ] A new Python script `app.py` is created to serve as the entry point for the Streamlit web application.
- [ ] The `requirements.txt` file is updated to include `streamlit` and any other necessary web-related dependencies (e.g., `pandas` for data display).
- [ ] The web interface includes a file uploader widget (`st.file_uploader`) supporting `.txt` and `.md` file formats.
- [ ] Upon file upload, the application correctly integrates with existing analysis logic in `story/analysis.py` (word count, reading time, character identification) and `story/narrative.py` (setup & payoff detection).
- [ ] Analysis results are displayed interactively within the Streamlit app:
    - Basic metrics (word count, reading time) shown as dashboard-style metrics.
    - Character identification results displayed in a clear, sortable table.
    - Narrative analysis (setups and payoffs) presented in an organized format (e.g., expandable sections or a summary list).
- [ ] A "Download Report" button is implemented to allow users to export the full analysis as a Markdown file.
- [ ] The application includes basic error handling for file uploads and LLM processing (e.g., if Ollama is not running).
- [ ] Documentation (e.g., in `README.md` or a new `WEB_APP.md`) is updated to explain how to run the Streamlit app locally.

## Technical Notes
- **Architectural Choice:** Streamlit was chosen for its Python-centric approach, which aligns with the project's existing codebase and allows for rapid development of data-focused UIs. It also provides a straightforward path for adding authentication (e.g., via `streamlit-authenticator`) in future iterations.
- **Integration:** The `app.py` should import and reuse functions from the `story/` package to ensure consistency between the CLI and web interfaces.
- **State Management:** Streamlit's session state will be used to manage uploaded data and analysis results during a user session.
- **Styling:** Vanilla Streamlit components will be used initially, with custom CSS added only where necessary for clarity or branding.
- **Ollama Dependency:** The web app will require a running Ollama instance, similar to the CLI tool. Clear instructions or UI-based checks should be provided to the user.
