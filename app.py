import streamlit as st
import fitz  # PyMuPDF
from search_engine import build_search_index, search

st.set_page_config(page_title="AI PDF Search", layout="wide")
st.title("🔍 AI Document Search Engine")

# Upload PDF(s)
uploaded_files = st.file_uploader("📄 Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

# Extract text from PDF
def extract_text_from_uploaded_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Build search index
if st.button("⚙️ Load and Index PDFs"):
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.getvalue()
            text = extract_text_from_uploaded_pdf(file_bytes)

            # Debug: show preview
            st.write(f"🧪 Preview of extracted text from {uploaded_file.name}:")
            st.code(text[:500])  # preview first 500 chars

            documents.append({
                "text": text,
                "source": uploaded_file.name
            })

        if documents:
            index, metadata = build_search_index(documents)
            st.session_state.index = index
            st.session_state.metadata = metadata
            st.success(f"✅ Indexed {len(documents)} documents")
        else:
            st.error("❌ No text extracted.")
    else:
        st.warning("⚠️ Please upload PDFs first.")

# Search section
if "index" in st.session_state:
    query = st.text_input("🔎 Enter your search query")
    if query:
        results = search(query, st.session_state.index, st.session_state.metadata)
        st.subheader("📌 Top Matches:")
        if results:
            for r in results:
                st.markdown(f"📄 **{r['source']}**")
                st.write(r['text'])
                st.markdown("---")
        else:
            st.warning("😕 No relevant results found.")
else:
    st.info("👆 Upload and index PDFs to start searching.")
