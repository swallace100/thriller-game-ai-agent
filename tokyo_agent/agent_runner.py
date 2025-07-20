from agents import Agent, Runner
from dotenv import load_dotenv
import os
from .indexing_utils import load_faiss_index, search_faiss_index
from .data_utils import extract_text_from_pdfs

load_dotenv(dotenv_path='./resources/openaiApiKey.env')
api_key = os.getenv("OPENAI_API_KEY")

# Query example
def run_agent(index, texts):
    query = "When is burnable trash collected in Shibuya?"
    context = search_faiss_index(index, texts, query)

    agent = Agent(
        name="TokyoLifeGuide",
        instructions=f"You have this info to work from: {context}. Answer questions clearly and practically."
    )

    result = Runner.run_sync(agent, query)
    print(result.final_output)
