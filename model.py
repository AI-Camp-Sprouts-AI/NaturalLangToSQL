from langchain.schema.language_model import BaseLanguageModel

def load_model(model_type: str, model_name: str, api_key: str, *args, **kwargs) -> BaseLanguageModel:
    """
    Load and return a language or chat model based on the specified model type and name.

    This function dynamically imports and creates an instance of the specified model type 
    with the provided model name and API key. Additional arguments and keyword arguments
    are passed to the model's constructor.

    :param str model_type: The type of the model to load. Supported model types include 
                       "huggingface", "openai", "googlepalm", 
                       "chatopenai", "chatanthropic" and "jinachat".
    :param str model_name: The name or identifier of the model to load.
    :param str api_key: The API key to use when initializing the model.
    :param args: Additional positional arguments to pass to the model's constructor.
    :param kwargs: Additional keyword arguments to pass to the model's constructor.
    :return: An instance of the specified model.
    :raises ValueError: If the specified model type is not supported.

    Example usage:
        model = load_model("openai", "text-davinci-003", "XXXXXXXXXXXXX", temperature=0.1)
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
        return GooglePalm(model_name=model_name, google_api_key=api_key, *args, **kwargs)

    # Chat Models    
    if model_type == "chatopenai": # gpt-4, gpt-4-0613, gpt-4-32k, gpt-4-32k-0613, gpt-3.5-turbo, gpt-3.5-turbo-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-16k-0613
        from langchain.chat_models import ChatOpenAI
        return ChatOpenAI(model=model_name, openai_api_key=api_key, *args, **kwargs)
    
    if model_type == "chatanthropic": # no model names
        from langchain.chat_models import ChatAnthropic
        return ChatAnthropic(model_name=model_name, anthropic_api_key=api_key, *args, **kwargs)
    
    if model_type == "jinachat": # no model names
        from langchain.chat_models import JinaChat
        return JinaChat(jinachat_api_key=api_key, *args, **kwargs)
    
    raise ValueError(f"No model found for type '{model_type}'.")