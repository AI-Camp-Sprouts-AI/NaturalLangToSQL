from dotenv import load_dotenv
from os import getenv
from model import load_embeddings_model
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def _load_api_structure() -> list:
    """
    Load the API structure from a text file and split it into manageable chunks using a text splitter.

    Returns:
        list: A list of API structure chunks.
    """

    api_structure = ""

    # Read API structure from file
    with open("api_structure.txt", "r") as file:
        api_structure = file.read().strip()

    # Split the API structure into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )

    texts = text_splitter.create_documents([api_structure])

    return texts

def embed_api_structure():
    """
    Embed the API structure into a FAISS index and save it locally.
    """

    # Load environment variables
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')

    # Load embeddings model
    embeddings_model = load_embeddings_model("openai", api_key)

    # Retrieve the API structure
    api_structure = _load_api_structure()

    # Embed the API structure into a FAISS index
    index = FAISS.from_documents(api_structure, embeddings_model)

    # Save the FAISS index locally
    index.save_local("index")

def get_relevant_api_calls(query: str, top_k: int) -> list:
    """
    Search the embedded API structure for relevant API calls based on the provided query.

    Args:
        query (str): The search query.
        top_k (int): The number of top relevant API calls to retrieve.

    Returns:
        list: A list of relevant API calls.
    """

    # Load environment variables
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')

    # Load embeddings model
    embeddings_model = load_embeddings_model("openai", api_key)

    # Load the FAISS index locally
    index = FAISS.load_local("index", embeddings_model)

    # Search the FAISS index for relevant API calls
    docs = index.similarity_search(query, top_k)

    return [doc.page_content for doc in docs]