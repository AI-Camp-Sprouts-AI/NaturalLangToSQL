from model import load_llm_model
from embed import get_relevant_api_calls
import json

class LLMFactory:
    """
    Factory Class for LLM (Language to API Model) Initialization with API Keys.
    
    Attributes:
        api_key (str): The API key to authenticate and initialize the model.
    """

    def __init__(self, api_key: str):
        """
        Initialize the LLMFactory with the given API key.

        Args:
            api_key (str): The API key to authenticate and initialize the model.
        """
        self.api_key = api_key

    def create_llm_instance(self, model_type: str, model_name: str) -> 'LLM':
        """
        Create and return an instance of LLM.

        Args:
            model_type (str): The type of the model to be loaded.
            model_name (str): The name of the model to be loaded.

        Returns:
            LLM: An instance of the LLM class initialized with the specified model and API key.
        """
        return LLM(model_type, model_name, self.api_key)


class LLM:
    """
    Language to API Model class that provides functionality to convert natural language commands into structured API calls.

    Attributes:
        model: The loaded language model instance.
        template (str): A template used to structure the prompt for the language model.
    """

    def __init__(self, model_type: str, model_name: str, api_key: str):
        """
        Initialize the LLM with the given model type, model name, and API key.

        Args:
            model_type (str): The type of the model to be loaded.
            model_name (str): The name of the model to be loaded.
            api_key (str): The API key to authenticate and initialize the model.
        """

        self.model = load_llm_model(model_type, api_key, model_name, temperature=0)

        # Define a consistent template for the model prompt.
        self.template = """
            You are an advanced API interpreter. Your task is to extract the HTTP method, endpoint, and body of the API request from the provided command.
            Given the API structure and a detailed command, parse the command to identify these elements of the API request. Respond with each element in a structured format.
            If the command is not valid or unclear, respond with "INVALID QUESTION".

            For example, for a command "Update the name and status of pet 112 to 'Buddy' and 'sold' respectively.", the response is:
            "method": "POST",
            "endpoint": "/pet/112",
            "body": (
                "name": "Buddy",
                "status": "sold"
            )

            If the body should be empty, leave it as ().
            Do not respond with anything besides the method, endpoint, and body.

            API Structure:
            {relevant_api}
            Command:
            {command}
        """.replace('  ', '').strip()
    
    def convert_text_to_command(self, text: str) -> dict:
        """
        Convert the given text to a structured API command using the language model.

        Args:
            text (str): The natural language command to be converted.

        Returns:
            str: The converted API command in a structured format.
        """

        if not self.model:
            return "Model must be initialized before query."
        if len(text) == 0:
            return "I did not understand. Can you please provide more details?"
        if text[-1] != '.' and text[-1] != '?':
            text += "."

        # Retrieve relevant API calls and format the prompt.
        relevant_api = '\nNEW LINE\n'.join(get_relevant_api_calls(text, 2)).replace('{', '(').replace('}', ')')
        prompt = self.template.format(relevant_api=relevant_api, command=text)
        response = self.model.predict(prompt)

        # Handle invalid responses.
        if "INVALID QUESTION" in response:
            return "I did not understand. Can you please provide more details?"
        
        # Convert the response to a structured format.
        response = response.replace('(', '{').replace(')', '}')
        dict = json.loads('{' + response + '}')
        return dict