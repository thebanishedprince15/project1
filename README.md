# Deployable Agent 2 (Creative Brief → Google Drive)

## Features
- Runs on Streamlit Cloud / Render
- Uses HuggingFace model instead of Ollama
- Creates folders in Google Drive
- Designed for public deployment

## Setup
1. Set your Hugging Face API key inside `brief_parser.py`
2. Place your `credentials.json` file in the root folder
3. Run:
   streamlit run streamlit_ui/brief_ui.py

4. On first Google login, approve the app
5. Use `token.json` for re-authentication persistence