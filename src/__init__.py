import re
import importlib
from os import getenv
from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pathlib import Path
from glob import glob

from .database_connector import execute_command
from .main import initialize_model
from .mock_data_generator import add_mock_data_to_db
from langchain.chat_models import ChatOpenAI

CWD = Path(__file__).parent

PATH_TO_FAKE_DATASTRUCTURES = CWD.joinpath('../data/fake_data_structures')


def create_terminal_instance():
    """
    Creates a terminal instance
    1. Mimics the exact scenario in which the user will use this package
    """
    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",
                     openai_api_key=api_key, temperature=0)
    model = initialize_model(llm=llm, options={'memory': 3, 'review': True})
    model.load_schema_from_file(CWD.joinpath('../data/schema.txt').absolute())

    while True:
        user_input = input("Enter something (or type 'exit' to close): ")
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'
        else:
            output = model.predict(user_input)
            if output.is_final_output:
                print("Query : \n\"", output.message + '"\n')
                print("Output : \n", execute_command(output.message))
                print('-'*80 + '\n')
            else:
                print(output.message)

    """
    4. Create a function which takes the input and output from these testcases and outputs the accuracy of the model. This testing function has to be written here (run_test_suites()
    5. The answer generated must be vetted for accuracy (reruns must provide the same result). Publish the accuracy.

    # Function to calculate accuracy
    def calculate_accuracy(test_cases):
        correct = 0
        for test_case in test_cases:
            if test_case['output'] == test_case['sql_output']:
                correct += 1
        accuracy = correct / len(test_cases) * 100
        return accuracy

    # Calculate accuracy
    accuracy = calculate_accuracy(test_cases)
    print(f"Accuracy: {accuracy:.2f}%")
    """


def run_test_suites():
    """
    This function should use the testcase_runner.py module to run the testcases

    This function should get inputs:
    1. List down all the test files for the user to select

    """
    print("Run the test suites here...")
    # Call the testcase_runner file here


def create_mock_data():
    """
    This function should use the mock_data_generator.py module
    to create the mock data.

    The data structures will be listed under the file format
        <table_name>.py

    This function should get two inputs
    1. List down all the data structure files for the user to select
    2. Ask how many number of fake data has to be generated

    """
    fake_data_files = glob(
        './*.py', root_dir=PATH_TO_FAKE_DATASTRUCTURES.absolute())
    table_name = inquirer.rawlist(
        message="Choose the Table Name",
        choices=[
            re.sub(r'(^\./|\.py$)', '', filename) for filename in fake_data_files
        ]
    ).execute()
    num_of_fake_data_to_generate = int(inquirer.number(
        message="Enter the number of fake data to generate: ",
        min_allowed=1,
    ).execute())

    module_name = f'data.fake_data_structures.{table_name}'

    try:
        module = importlib.import_module(module_name)
        output = module.main()
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found.")

    column_blueprint = output.get('column_blueprint')
    fake_data_structure = output.get('fake_data_structure')

    add_mock_data_to_db(table_name, column_blueprint,
                        fake_data_structure, num_of_fake_data_to_generate)
