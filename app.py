import streamlit as st
import fitz  # PyMuPDF
from search_engine import build_search_index, search

st.title("🔍 AI Document Search Engine")

# Step 1: Upload PDF files
uploaded_files = st.file_uploader("📄 Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

# Step 2: Extract text from uploaded files
def extract_text_from_uploaded_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Step 3: Build search index from uploaded PDFs
if st.button("⚙️ Load and Index Uploaded PDFs"):
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            text = extract_text_from_uploaded_pdf(uploaded_file)
            documents.append({
                "text": text,
                "source": uploaded_file.name
            })

        index, metadata = build_search_index(documents)
        st.session_state.index = index
        st.session_state.metadata = metadata
        st.success(f"✅ Indexed {len(documents)} PDF files.")
    else:
        st.warning("Please upload at least one PDF.")

# Step 4: Semantic search
if "index" in st.session_state:
    query = st.text_input("🔎 Enter your search query")
    if query:
        results = search(query, st.session_state.index, st.session_state.metadata)
        st.subheader("📌 Top Matches:")
        if results:
            for r in results:
                st.write(f"📄 **{r['source']}**")
                st.write(r['text'])
                st.markdown("---")
        else:
            st.warning("No matching results found.")
else:
    st.info("👆 Upload and index some PDFs first.")
