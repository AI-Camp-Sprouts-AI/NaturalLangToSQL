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

        self.schema = ''
        self.system_prompt = """
        You are PostGreSQL Expert. You have to respond with PostGreSQL commands for the QUESTION asked by the user based on the DATABASE SCHEMA. 
        Make sure to follow the 'IMPORTANT NOTE' and 'GUIDELINES' provided. ALWAYS REMEMBER TO FOLLOW 'IMPORTANT NOTE' & 'GUIDELINES', DO NOT DEVIATE FROM IT.
        If you can't answer the question or if the question is irrelevant to the Database Schema, Say 'I don't know'. Don't respond anything else.
        If a question is incomplete, ambiguous, unclear, or unrelated to the provided database, ASK FOR CLARIFICATION INSTEAD OF RESPONDING WITH PostGreSQL QUERY
        If a question is missing any necessary information, ASK FOR CLARIFICATION INSTEAD OF RESPONDING WITH PostGreSQL QUERY
        
        IMPORTANT NOTE:
        1. Always use ILIKE operators for comparing string

        DATABASE SCHEMA:
        {schema}
        
        Answer using the following Template
        {{Your PostGreSQL Command}}
        """.replace('  ', '').strip()

        self.review_prompt = """
            You are to review the content provided. Your objective is clear:
            If the content contains an SQL query, extract and present only that SQL query.
            If the content does not contain any SQL query, respond with 'INVALID QUERY'.
            Do not provide additional information or context. Stick strictly to the above guidelines.
        """.replace('  ', '').strip()

        self.chat_history = []
        self.memory_length = options['memory']*2 if 'memory' in options else 0

    def predict(self, user_input: str) -> ModelOutput:
        if len(self.schema) == 0:
            raise Exception('Schema not loaded. Please load the database schema using `model.load_schema_from_file` or `model.load_schema_as_string`')
        if len(user_input) == 0:
            return ModelOutput("I'm sorry, I don't understand your question.", False)
        if user_input[-1] not in '.;:?!':
            user_input += '.'

        system_prompt = self.system_prompt.format(schema=self.schema)
        messages = [SystemMessage(content=system_prompt),
                    HumanMessage(content=user_input)]
        response = self.llm.predict_messages(
            messages=(self.chat_history + messages))

        final_output = False

        if self.options.get('review', False):
            new_response = self.llm.predict_messages(messages=[SystemMessage(
                content=self.review_prompt), HumanMessage(content="Content:\n"+response.content)])
            if 'INVALID' not in new_response.content:
                final_output = True
                response = new_response

        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response.content))
        if len(self.chat_history) > self.memory_length:
            excess = len(self.chat_history) - self.memory_length
            self.chat_history = self.chat_history[excess:]

        return ModelOutput(response.content, final_output)

    def override_system_prompt(self, new_system_prompt: str) -> None:
        if '{schema}' in new_system_prompt:
            self.system_prompt = new_system_prompt

    def override_review_prompt(self, new_review_prompt: str) -> None:
        self.review_prompt = new_review_prompt

    def load_schema_from_file(self, file_path: str) -> bool:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            self.load_schema_as_string(contents)

    def load_schema_as_string(self, schema: str) -> bool:
        self.schema = schema

    def clear_chat_history(self) -> None:
        self.chat_history = []

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
