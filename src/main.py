from .interfaces import IBaseClass, ModelOutput
from enum import Enum
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Enumerators
OutputTypes = Enum('OutputTypes', [
    'SQL',
    # 'API' # This is for a later use case
])


class NLP2SQL(IBaseClass):
    """
    This class implements the Natural Language to the SQL 
    functionality of the package
    """
    system_prompt: str
    schema: str
    options: dict
    llm: BaseLanguageModel

    def __init__(self, llm, options) -> None:
        self.llm = llm
        self.options = options

        self.schema = 'A normal SQL schema related to the question.'
        self.system_prompt = """
            You are an experienced data analyst with specialized knowledge in SQL databases and queries. 
            You can provide accurate SQL queries based on the provided database schema and make use of your expert knowledge of SQL and databases.
            The purpose is to assist with formulating SQL queries based on the information available, maintaining the accuracy and relevance of the responses.
            For valid and clear questions related to the provided database, provide ONLY the appropriate SQL query as a response and nothing else.
            If a question is asked that is incomplete, ambiguous, unclear, or unrelated to the provided database, ask for clarification.
            Database Schema:
            {schema}
        """.replace('  ', '').strip()

        self.chat_history = []
        self.memory_length = options['memory']*2 if 'memory' in options else 0

    def predict(self, user_input: str) -> ModelOutput:
        if user_input[-1] not in '.;:?!':
            user_input += '.'
        
        system_prompt = self.system_prompt.format(schema=self.schema)
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_input)]
        response = self.llm.predict_messages(messages=(self.chat_history + messages))

        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response.content))
        if len(self.chat_history) > self.memory_length:
            excess = len(self.chat_history) - self.memory_length
            self.chat_history = self.chat_history[excess:]

        return ModelOutput(response.content, True)

    def override_system_prompt(self, new_system_prompt: str) -> None:
        if '{schema}' in new_system_prompt:
            self.system_prompt = new_system_prompt

    def load_schema_from_file(self, file_path: str) -> bool:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            self.load_schema_as_string(contents)

    def load_schema_as_string(self, schema: str) -> bool:
        self.schema = schema

# Can be implemented later


# class NLP2API(IBaseClass):
#     def __init__(self) -> None:
#         pass

#     def predict(self, user_input: str) -> ModelOutput:
#         pass

#     def load_context_from_file(self, file_path: str) -> bool:
#         pass

#     def load_context_as_string(self, context: str) -> bool:
#         pass


output_type_class_map = {
    OutputTypes.SQL: NLP2SQL,
    # OutputTypes.API: NLP2API,
}


def initialize_model(llm, options={}, output_type: OutputTypes = OutputTypes.SQL):
    """
    Based on the Output Type the Model will be instantiated
    """

    model_class = output_type_class_map[output_type]
    model_instance = model_class(llm, options)
    return model_instance