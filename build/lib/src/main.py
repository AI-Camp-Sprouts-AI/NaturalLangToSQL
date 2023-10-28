
from .interfaces import IBaseClass, ModelOutput
from enum import Enum

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
    llm: any  # This any has to be changed to the LangChain LLM Type

    def __init__(self, llm, options) -> None:
        self.llm = llm
        self.options = options
        # Initialize the system_prompt here
        # Any other required preprocessing has to be done here
        pass

    def predict(self, user_input: str) -> ModelOutput:
        # This function should run the predict api function on the
        # llm and return the output
        pass

    def override_system_prompt(self, new_system_prompt: str) -> None:
        # This function is mainly used for testing multiple system
        # prompts from the testing module
        # - Low Priority
        pass

    def load_schema_from_file(self, file_path: str) -> bool:
        # This function should load the schema from the file into the prompt
        # This function should call the load_schema_as_string function
        # once the file has been read
        pass

    def load_schema_as_string(self, schema: str) -> bool:
        # The value of the schema has to be stored in the schema object
        # Any text preprocessing of the schema has to be done here
        pass

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


def initialize_model(llm, options={}, output_type: OutputTypes = 'SQL'):
    """
    Based on the Output Type the Model will be instantiated
    """

    model_class = output_type_class_map[output_type]
    model_instance = model_class(llm, options)
    return model_instance
