import streamlit as st
from utils import load_documents_from_folder
from search_engine import build_search_index, search

st.title("🔍 AI Document Search Engine")

folder_path = st.text_input("Enter folder path with PDF files", "docs")

# Load and store index using session_state
if st.button("Load and Index Documents"):
    with st.spinner("Loading and indexing..."):
        documents = load_documents_from_folder(folder_path)
        index, metadata = build_search_index(documents)
        st.session_state.index = index
        st.session_state.metadata = metadata
        st.success("✅ Documents indexed successfully!")

# Search section – Always visible if index is loaded
if "index" in st.session_state:
    query = st.text_input("Enter your search query")
    if query:
        results = search(query, st.session_state.index, st.session_state.metadata)
        st.subheader("🔎 Top Matches:")
        for r in results:
            st.write(f"📄 **{r['source']}**")
            st.write(r['text'])
            st.markdown("---")
else:
    st.info("👆 Please load documents before searching.")
