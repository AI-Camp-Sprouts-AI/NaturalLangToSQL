from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from os import getenv
from model import load_model
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
        self.model_type = model_type
        self.model_name = model_name
        self.api_key = api_key
        self.api_structure = None

    def _initialize_chain(self):
        # Model
        model = load_model(self.model_type, self.model_name, self.api_key, temperature=0)

        template = """
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
            {api_structure}
            Command: {{command}}
        """.replace('  ', '').format(api_structure=api_structure.replace('{', '(').replace('}', ')')).strip()

        prompt = PromptTemplate(
            input_variables=["command"], 
            template = template
        )

        self.chain = LLMChain(llm=model, prompt=prompt)

    def load_api_structure_as_string(self, api_structure_str: str):
        self.api_structure = api_structure_str.strip()
        self._initialize_chain()


    def load_api_structure_from_file(self, api_structure_file: str):
        with open(api_structure_file, 'r') as file:
            self.api_structure = file.read().strip()
        self._initialize_chain()  

    def convert_text_to_command(self, text: str):
        if not self.chain:
            return "Chain must be initialized before query."
        if len(text) == 0:
            return "I did not understand. Can you please provide more details?"
        if text[-1] != '.' and text[-1] != '?':
            text += "."

        response = self.chain.run(command=text)
        if "INVALID QUESTION" in response:
            return "I did not understand. Can you please provide more details?"
        response = response.replace('(', '{').replace(')', '}')
        dict = json.loads('{' + response + '}')
        return str(dict)

    def visualize_data(self, dataframe):
        print(dataframe)

    def refine_query(self, text: str):
        refined_query = text
        return refined_query

# Example usage
if __name__ == '__main__':
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')

    api_structure = ""
    with open("api_structure.txt", "r") as file:
        api_structure = file.read().strip()

    factory = LLMFactory(api_key)

    while True:
        # model_type = input("Model Type: ").lower().strip()
        # model_name = input("Model Name: ").lower().strip()
        model_type = "chatopenai"
        model_name = "gpt-4-0613"
        llm_instance = factory.create_llm_instance(model_type=model_type, model_name=model_name)
        llm_instance.load_api_structure_as_string(api_structure)
        text = input("Prompt: ")
        # text = "Update the status of pet 789 to 'available'."
        print(llm_instance.convert_text_to_command(text) + '\n')