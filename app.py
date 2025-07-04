import streamlit as st
import fitz  # PyMuPDF
from search_engine import build_search_index, search

st.set_page_config(page_title="AI PDF Search Engine", layout="wide")
st.title("🔍 AI Document Search Engine (with Upload)")

# Upload PDF(s)
uploaded_files = st.file_uploader("📄 Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

# Extract text from PDF
def extract_text_from_uploaded_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Build search index from uploaded files
if st.button("⚙️ Load and Index Uploaded PDFs"):
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            text = extract_text_from_uploaded_pdf(uploaded_file)
            st.write(f"📄 {uploaded_file.name}: {len(text)} characters extracted")  # DEBUG
            documents.append({
                "text": text,
                "source": uploaded_file.name
            })

        if documents:
            index, metadata = build_search_index(documents)
            st.session_state.index = index
            st.session_state.metadata = metadata
            st.success(f"✅ Indexed {len(documents)} files.")
        else:
            st.error("❌ No text extracted from uploaded PDFs.")
    else:
        st.warning("⚠️ Please upload one or more PDFs first.")

# Search query input
if "index" in st.session_state:
    query = st.text_input("🔎 Enter your search query")
    if query:
        results = search(query, st.session_state.index, st.session_state.metadata)
        st.subheader("📌 Top Matches")
        if results:
            for r in results:
                st.markdown(f"📄 **{r['source']}**")
                st.write(r['text'])
                st.markdown("---")
        else:
            st.warning("😕 No relevant results found.")
else:
    st.info("👆 Upload and index your PDFs to start searching.")
