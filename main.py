import openai
from dotenv import load_dotenv
from os import getenv

class LLMFactory:
    """
    Factory Class for LLM Initialization with API Keys
    """
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def create_llm_instance(self):
        return LLM()


class LLM:
    """
    Main Class - created with the instance of the Factory Class
    """

    def __init__(self):
        self.schema = None

    def load_schema_as_string(self, schema_str):
        """
        Load Schema as String
        """
        self.schema = schema_str

    def load_schema_from_file(self, schema_file):
        """
        Load Schema from File
        """
        self.schema = "" # placeholder

    def convert_text_to_sql(self, prompt):
        """
        Convert Text to SQL
        """
        # https://platform.openai.com/docs/guides/gpt openai documentation
        model = "gpt-3.5-turbo-0613"
        messages = [
            {"role": "system", "content": ""}, # Sets behavior
            {"role": "user", "content": prompt}, # User question/prompt
            {"role": "assistant", "content": ""} # Conversation history, schema, useful data
        ]
        response = openai.ChatCompletion.create(model=model, messages=messages)
        sql_query = response["choices"][0]["message"]["content"]
        return sql_query

    def visualize_data(self, dataframe):
        """
        Visualize Data
        """
        print(dataframe) # placeholder

    def refine_query(self, prompt):
        """
        Refine Query
        """
        refined_query = prompt # placeholder
        return refined_query


# Example usage
if __name__ == '__main__':
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')

    factory = LLMFactory(api_key=api_key)
    llm_instance = factory.create_llm_instance()
    llm_instance.load_schema_from_file('schema.sql')

    prompt = input()
    sql = llm_instance.convert_text_to_sql(prompt)
    print(sql)