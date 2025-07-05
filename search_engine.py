from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
import re


def split_into_chunks(text, max_tokens=200):
    """
    Split the text into chunks for embedding. 
    This uses simple paragraph or sentence-based splitting.
    """
    # Split by double newlines or periods
    raw_chunks = re.split(r'\n\n|\.\s', text)
    cleaned_chunks = [chunk.strip() for chunk in raw_chunks if len(chunk.strip()) > 20]

    # Optional: further truncate long chunks
    final_chunks = []
    for chunk in cleaned_chunks:
        if len(chunk.split()) > max_tokens:
            sentences = chunk.split(". ")
            current = ""
            for sentence in sentences:
                if len((current + sentence).split()) <= max_tokens:
                    current += sentence + ". "
                else:
                    final_chunks.append(current.strip())
                    current = sentence + ". "
            final_chunks.append(current.strip())
        else:
            final_chunks.append(chunk)

    return final_chunks


def build_search_index(documents):
    """
    Build FAISS index from list of documents. Each document is a dict with 'text' and 'source'.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = []
    metadata = []

    for doc in documents:
        chunks = split_into_chunks(doc["text"])
        for chunk in chunks:
            texts.append(chunk)
            metadata.append({
                "text": chunk,
                "source": doc["source"]
            })

    # Generate embeddings
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, metadata


def search(query, index, metadata, top_k=5):
    """
    Search the query using the FAISS index and return top_k results.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query, convert_to_numpy=True)
    query_embedding = np.expand_dims(query_embedding, axis=0)

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, score in zip(indices[0], distances[0]):
        if i < len(metadata):
            results.append({
                "text": metadata[i]["text"],
                "source": metadata[i]["source"],
                "score": float(score)
            })

    return results
