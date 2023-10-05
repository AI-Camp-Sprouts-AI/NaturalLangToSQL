from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.embeddings import Embeddings

def load_llm_model(model_type: str, api_key: str, model_name: str = "", *args, **kwargs) -> BaseLanguageModel:
    """
    Load a specified language or chat model.

    Args:
        model_type (str): Type of the model ("huggingface", "openai", etc.).
        api_key (str): API key for model initialization.
        model_name (str, optional): Model identifier. Defaults to "".
        *args: Positional arguments for the model.
        **kwargs: Keyword arguments for the model.

    Returns:
        BaseLanguageModel: Loaded model instance.

    Raises:
        ValueError: If the model type is unsupported.

    Example:
        >>> llm_model = load_llm_model("openai", "API_KEY", "text-davinci-003", temperature=0.1)
    """

    # LLMS
    if model_type == "huggingface": # any huggingface repo id
        from langchain.llms import HuggingFaceHub
        return HuggingFaceHub(repo_id=model_name, huggingfacehub_api_token=api_key, task="text2text-generation", *args, **kwargs)
    
    if model_type == "openai": # text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
        from langchain.llms import OpenAI
        return OpenAI(model=model_name, openai_api_key=api_key, *args, **kwargs)

    if model_type == "googlepalm": # text-bison-001, chat-bison-001, embedding-gecko-001, embedding-gecko-002
        from langchain.llms import GooglePalm
        return GooglePalm(model_name="models/"+model_name, google_api_key=api_key, *args, **kwargs)

    # Chat Models    
    if model_type == "chatopenai": # gpt-4, gpt-4-0613, gpt-4-32k, gpt-4-32k-0613, gpt-3.5-turbo, gpt-3.5-turbo-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-16k-0613
        from langchain.chat_models import ChatOpenAI
        return ChatOpenAI(model=model_name, openai_api_key=api_key, *args, **kwargs)
    
    if model_type == "chatanthropic": # no model names
        from langchain.chat_models import ChatAnthropic
        return ChatAnthropic(anthropic_api_key=api_key, *args, **kwargs)
    
    if model_type == "jinachat": # no model names
        from langchain.chat_models import JinaChat
        return JinaChat(jinachat_api_key=api_key, *args, **kwargs)
    
    raise ValueError(f"No model found for type '{model_type}'.")

def load_embeddings_model(model_type: str, api_key: str, model_name: str = "", *args, **kwargs) -> Embeddings:
    """
    Load a specified embeddings model.

    Args:
        model_type (str): Type of the model ("huggingface", "openai", etc.).
        api_key (str): API key for model initialization.
        model_name (str, optional): Model identifier. Defaults to "".
        *args: Positional arguments for the model.
        **kwargs: Keyword arguments for the model.

    Returns:
        Embeddings: Loaded embeddings model instance.

    Raises:
        ValueError: If the model type is unsupported.

    Example:
        >>> embeddings_model = load_embeddings_model("openai", "API_KEY")
    """

    if model_type == "huggingface": # any huggingface repo id
        from langchain.embeddings import HuggingFaceHubEmbeddings
        return HuggingFaceHubEmbeddings(huggingfacehub_api_token=api_key, repo_id=model_name, task="feature-extraction", *args, **kwargs)
    
    if model_type == "openai": # no model names
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings(openai_api_key=api_key, *args, **kwargs)

    if model_type == "googlepalm": # no model names
        from langchain.embeddings import GooglePalmEmbeddings
        return GooglePalmEmbeddings(google_api_key=api_key, *args, **kwargs)
    
    raise ValueError(f"No model found for type '{model_type}'.")