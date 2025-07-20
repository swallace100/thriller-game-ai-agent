from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(all_texts)
embeddings = np.array(embeddings).astype('float32')

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save the index
faiss.write_index(index, './resources/shibuya_trash.index')

# Save the texts so you can retrieve them later by index
import pickle
with open('./resources/shibuya_trash_texts.pkl', 'wb') as f:
    pickle.dump(all_texts, f)
