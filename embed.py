from dotenv import load_dotenv
from os import getenv
from model import load_embeddings_model
from yaml import safe_load
from langchain.vectorstores import FAISS
from langchain.schema.document import Document

def _load_api_structure():
    api_structure = ""
    with open("api_structure.txt", "r") as file:
        api_structure = file.read().strip()

    api_data = safe_load(api_structure)
    paths = api_data.get("paths", {})

    api_strings = []

    for path, methods in paths.items():
        for method, details in methods.items():
            details_str = f"{path} ({method.upper()}):\n" + "\n".join([f"{k}: {v}" for k, v in details.items()])
            api_strings.append(details_str)

    return api_strings

def embed_api_structure():
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')
    embeddings_model = load_embeddings_model("openai", api_key)

    api_structure = _load_api_structure()
    api_structure = [Document(page_content=api) for api in api_structure]

    index = FAISS.from_documents(api_structure, embeddings_model)
    index.save_local("index")

def get_relevant_api_calls(query: str, top_k: int):
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')
    embeddings_model = load_embeddings_model("openai", api_key)

    index = FAISS.load_local("index", embeddings_model)

    docs = index.similarity_search(query, top_k)

    return [doc.page_content for doc in docs]

if __name__ == '__main__':
    #embed_api_structure()
    text = input("Prompt: ")
    print(get_relevant_api_calls(text, 3))