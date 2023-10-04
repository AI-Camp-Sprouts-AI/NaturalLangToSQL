from model import load_llm_model
from embed import get_relevant_api_calls
import json

class LLMFactory:
    """
    Factory Class for LLM Initialization with API Keys
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    def create_llm_instance(self, model_type: str, model_name: str):
        return LLM(model_type, model_name, self.api_key)


class LLM:
    """
    Main Class - created with the instance of the Factory Class
    """
    def __init__(self, model_type: str, model_name: str, api_key: str):
        self.model = load_llm_model(model_type, api_key, model_name, temperature=0)

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
    
    def convert_text_to_command(self, text: str):
        if not self.model:
            return "Model must be initialized before query."
        if len(text) == 0:
            return "I did not understand. Can you please provide more details?"
        if text[-1] != '.' and text[-1] != '?':
            text += "."

        relevant_api = '\n'.join(get_relevant_api_calls(text, 2)).replace('{', '(').replace('}', ')')
        prompt = self.template.format(relevant_api=relevant_api, command=text)
        response = self.model.predict(prompt)

        if "INVALID QUESTION" in response:
            return "I did not understand. Can you please provide more details?"
        
        response = response.replace('(', '{').replace(')', '}')
        dict = json.loads('{' + response + '}')
        return str(dict)