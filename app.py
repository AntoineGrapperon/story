import streamlit as st
import pandas as pd
import io
import os
from story.analysis import calculate_word_count, estimate_reading_time, identify_characters_with_ollama
from story.narrative import identify_setups, analyze_payoffs
from story.utils.text_chunking import chunk_text

st.set_page_config(page_title="Story Analysis Tool", page_icon="📖", layout="wide")

st.title("📖 Story Analysis Tool")
st.markdown("""
Upload your story text file to get a comprehensive analysis of word counts, 
estimated reading time, character frequencies, and narrative setups/payoffs.
""")

# Sidebar for configuration
st.sidebar.header("Configuration")
ollama_model = st.sidebar.text_input("Ollama Model", value="llama3.2:3b")
chunk_size = st.sidebar.number_input("Chunk Size (words)", value=1000, step=100)

uploaded_file = st.file_uploader("Choose a story file", type=["txt", "md"])

if uploaded_file is not None:
    # Read the file content
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    text_content = stringio.read()
    file_name = uploaded_file.name

    # Basic Metrics
    word_count = calculate_word_count(text_content)
    reading_time = estimate_reading_time(word_count)

    col1, col2 = st.columns(2)
    col1.metric("Word Count", f"{word_count:,}")
    col2.metric("Est. Reading Time", f"{reading_time} min")

    if st.button("Run Deep Analysis"):
        with st.spinner("Analyzing characters and narrative..."):
            # 1. Character Identification
            st.subheader("👥 Character Identification")
            text_chunks = chunk_text(text_content, chunk_size=chunk_size)
            characters = identify_characters_with_ollama(text_chunks, model=ollama_model)
            
            if characters:
                char_df = pd.DataFrame(list(characters.items()), columns=["Character", "Frequency"])
                char_df = char_df.sort_values(by="Frequency", ascending=False).reset_index(drop=True)
                st.dataframe(char_df, use_container_width=True)
            else:
                st.info("No characters identified.")

            # 2. Narrative Analysis (Setups & Payoffs)
            st.subheader("🎭 Narrative Analysis (Setups & Payoffs)")
            setups = identify_setups(text_content, ollama_model, chunk_size)
            
            if setups:
                results = analyze_payoffs(text_content, setups, ollama_model, chunk_size)
                
                for res in results:
                    with st.expander(f"{res['id']}: {res['description']} ({res['status']})"):
                        st.markdown(f"**Introduced At:** {res['location']}")
                        if res['status'] == "Paid Off":
                            st.success(f"**Payoff:** {res['payoff_description']}")
                            st.markdown(f"**Payoff Location:** {res['payoff_location']}")
                        else:
                            st.warning(f"**Status:** {res['status']}")
                            st.markdown(f"**Note:** {res['payoff_description']}")
                
                # Report Generation for Download
                report_content = f"# Analysis Report: {file_name}

"
                report_content += f"## Basic Metrics
- Word Count: {word_count}
- Est. Reading Time: {reading_time} min

"
                report_content += "## Characters
"
                for char, freq in characters.items():
                    report_content += f"- {char}: {freq}
"
                
                report_content += "
## Narrative Analysis
"
                for res in results:
                    report_content += f"### {res['id']}: {res['description']}
"
                    report_content += f"- Status: {res['status']}
"
                    report_content += f"- Intro: {res['location']}
"
                    if res['status'] == "Paid Off":
                        report_content += f"- Payoff: {res['payoff_description']}
"
                        report_content += f"- Payoff Loc: {res['payoff_location']}
"
                    report_content += "
"

                st.download_button(
                    label="Download Full Report",
                    data=report_content,
                    file_name=f"analysis_{file_name}.md",
                    mime="text/markdown"
                )
            else:
                st.info("No narrative setups identified.")

else:
    st.info("Please upload a text or markdown file to begin.")

# Instructions for Ollama
with st.expander("ℹ️ How to run this"):
    st.markdown(f"""
    1. Ensure **Ollama** is installed and running.
    2. Pull the required model: `ollama pull {ollama_model}`
    3. Install dependencies: `pip install -r requirements.txt`
    4. Run the app: `streamlit run app.py`
    """)
