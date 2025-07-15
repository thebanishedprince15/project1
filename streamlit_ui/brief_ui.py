import streamlit as st
from agent2.brief_parser import parse_brief
from agent2.gdrive_uploader import create_drive_folders

st.title("Creative Brief → Google Drive Folder Creator")

uploaded_file = st.file_uploader("Upload your creative brief (.txt)", type=["txt"])

if uploaded_file:
    brief_text = uploaded_file.read().decode("utf-8")
    st.subheader("Parsed Brief Summary")
    result = parse_brief(brief_text)

    if "error" in result:
        st.error(f"Failed to parse: {result['error']}")
    else:
        st.json(result)
        if st.button("Create Google Drive Folders"):
            links = create_drive_folders(result["deliverables"])
            st.success("Google Drive folders created!")
            for link in links:
                st.markdown(f"[📁 {link}]({link})")