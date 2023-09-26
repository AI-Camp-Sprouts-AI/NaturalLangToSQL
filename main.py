from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from dotenv import load_dotenv
from os import getenv

class LLMFactory:
    """
    Factory Class for LLM Initialization with API Keys
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def create_llm_instance(self):
        return LLM(self.api_key)


class LLM:
    """
    Main Class - created with the instance of the Factory Class
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.schema = None

    def _initialize_chain(self):
        model = OpenAI(openai_api_key = self.api_key, temperature=0)
        primer = """
You are an experienced data analyst with specialized knowledge in SQL databases and queries. 
You can provide accurate SQL queries based on the provided database schema and make use of your expert knowledge of SQL and databases.
The purpose is to assist with formulating SQL queries based on the information available, maintaining the accuracy and relevance of the responses.
For valid and clear questions related to the provided database, provide the appropriate SQL query as a response and nothing else.
If a question is asked that is incomplete, ambiguous, unclear, or unrelated to the provided database, respond with \"I did not understand.'\" and explain why you don't understand.
Database Schema:
{schema}
        """.format(schema=self.schema).strip()
        numbers = "\nAny numbers including {numbers} are valid.\n"
        prompt = PromptTemplate(
            input_variables=["question", "numbers"], 
            template = primer + numbers + "{question}"
        )
        self.chain = LLMChain(llm=model, prompt=prompt)

    def load_schema_as_string(self, schema_str):
        self.schema = schema_str.strip()
        self._initialize_chain()


    def load_schema_from_file(self, schema_file):
        with open(schema_file, 'r') as file:
            self.schema = file.read().strip()
        self._initialize_chain()

    def convert_text_to_sql(self, text):
        if not self.chain:
            return "Chain must be initialized before query."
        if len(text) == 0:
            return "I did not understand. Can you please provide more details?"
        if text[-1] != '.' and text[-1] != '?':
            text += "?"
        numbers = ', '.join((word[:-1] if word[:-1].isdigit() else word) for word in text.split() if word.isdigit() or word[:-1].isdigit())
        sql = self.chain.run(question=text, numbers=numbers).strip()
        return sql

    def visualize_data(self, dataframe):
        print(dataframe)

    def refine_query(self, text):
        refined_query = text
        return refined_query

schema = """
CREATE TABLE Books (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    AuthorID INT,   
    PublisherID INT,
    PublishedYear YEAR,
    ISBN VARCHAR(20),
    PageCount INT,
    Price DECIMAL(8,2),
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID)
);
"""

# Example usage
if __name__ == '__main__':
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')

    factory = LLMFactory(api_key=api_key)
    llm_instance = factory.create_llm_instance()
    llm_instance.load_schema_as_string(schema)

    text = input()
    # text = "Find the total price of books for each author, where the total price is greater than 100, for books published after the year 2000 and have a PageCount greater than 300. List the results by AuthorID. The result should include the AuthorID and the total price of the books."
    sql = llm_instance.convert_text_to_sql(text)
    print(sql)