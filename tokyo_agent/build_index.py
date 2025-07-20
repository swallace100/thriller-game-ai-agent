import os
from tokyo_agent.indexing_utils import save_faiss_index
from tokyo_agent.data_utils import extract_text_from_pdfs

INDEX_PATH = './resources/shibuya_trash.index'
TEXTS_PATH = './resources/shibuya_trash_texts.pkl'
PDF_DIR = './resources/documents'

texts = extract_text_from_pdfs(PDF_DIR)
save_faiss_index(texts, INDEX_PATH, TEXTS_PATH)

print("Indexing complete. Ready for use.")
