import os
from tokyo_agent.indexing_utils import load_faiss_index
from tokyo_agent.agent_runner import run_agent

INDEX_PATH = './resources/shibuya_trash.index'
TEXTS_PATH = './resources/shibuya_trash_texts.pkl'

index, texts = load_faiss_index(INDEX_PATH, TEXTS_PATH)
run_agent(index, texts)
