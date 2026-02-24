# story
Story helps you create good novels!

## Feature Roadmap

### Core Features
- 📈 Structural Heatmaps: Map your draft against classic frameworks like Freytag’s Pyramid or the Hero’s Journey.
- 👤 The Codex: An automated character tracker that flags inconsistencies in traits, physical descriptions, and goals across chapters.
- 🎭 Emotional Arc Mapping: Visualizes the "mood" of each scene to identify where the narrative tension peaks or plateaus.
- 🔫 Chekhov’s Gun Detector: Identify "orphan" plot points—items or clues introduced early on that never reach a resolution.
- 🧩 Trope Analysis: Scans for genre-specific clichés and suggests ways to subvert them.

## Setup and Prerequisites

To run the analysis tools, you will need to have [Ollama](https://ollama.com/) installed and configured.

### 1. Install Ollama

Download and install Ollama from the official website: [https://ollama.com/download](https://ollama.com/download)

Follow the instructions for your operating system (Windows, macOS, Linux, or **Android via Termux**).

### 2. Pull the Language Model

For character analysis and other LLM-driven features, we recommend using a model from the Llama3.2 family. Due to potential resource constraints on some devices (especially Android via Termux), a smaller or quantized version is often preferable for performance.

To pull a suitable model, open your terminal and run:

```bash
ollama pull llama3.2:3b # A balanced 3B parameter model
# If performance is an issue, consider a quantized version:
# ollama pull llama3.2:3b-instruct-q4_K_M # Example of a quantized 3B model
```
You can explore other available models and their quantizations on the [Ollama models page](https://ollama.com/library).

### 3. Run the Ollama Server

Once the model is downloaded, start the Ollama server. This needs to be running in the background for the analysis scripts to work.

```bash
ollama serve
```
Keep this terminal window open while you are using the story analysis tools.

**Note for Android/Termux Users:**
Performance can vary significantly on mobile devices. If you experience timeouts or slow processing:
*   Ensure no other resource-intensive applications are running.
*   Consider using a smaller or more heavily quantized LLM (e.g., `llama3.2:3b-instruct-q4_K_M`) for faster inference.
*   Increase the `character_profiling_timeout` parameter in `run_all_profiling.py` if individual character processing still times out (though this will not directly speed up the LLM).

## Usage

(Further usage instructions will go here, once the character profiling feature is fully integrated and stable.)
