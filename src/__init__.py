from .main import initialize_model
from langchain.llms import OpenAI


def create_terminal_instance():
    """
    Creates a terminal instance
    1. Mimics the exact scenario in which the user will use this package
    """
    print("Creating a Terminal Instance for testing in dev environment...")
    # llm = OpenAI(openai_api_key="sk-...")
    # model = initialize_model(llm=llm)
    while True:
        user_input = input("Enter something (or type 'exit' to close): ")
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'
        else:
            # output = model.predict(user_input)
            print("Output will be shown here: ")
    pass


def run_test_suites():
    print("Run the test suites here...")


def create_mock_data():
    print("Create the mock data here...")
