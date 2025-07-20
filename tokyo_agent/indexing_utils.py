import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def save_faiss_index(texts, index_path, texts_path):
    embeddings = model.encode(texts).astype('float32')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, index_path)
    with open(texts_path, 'wb') as f:
        pickle.dump(texts, f)

def load_faiss_index(index_path, texts_path):
    index = faiss.read_index(index_path)
    with open(texts_path, 'rb') as f:
        texts = pickle.load(f)
    return index, texts

def search_faiss_index(index, texts, query, k=1):
    query_embedding = model.encode([query]).astype('float32')
    D, I = index.search(query_embedding, k)

    # Returns the text chunk corresponding to the closest matching embedding.
    return texts[I[0][0]]
