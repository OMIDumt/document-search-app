from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, max_words=100):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def build_search_index(docs):
    all_chunks, metadata = [], []
    for filename, text in docs:
        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({"source": filename, "text": chunk})

    embeddings = model.encode(all_chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))
    return index, metadata

def search(query, index, metadata, top_k=5):
    query_emb = model.encode([query])
    D, I = index.search(np.array(query_emb).astype("float32"), top_k)
    results = []
    for idx in I[0]:
        results.append(metadata[idx])
    return results
