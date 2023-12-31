import re
import sys

from os import getenv
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from glob import glob

# Exports from Module
from .main import initialize_model
from .database_connector import execute_command, connect_and_execute_command

CWD = Path(__file__).parent

PATH_TO_FAKE_DATASTRUCTURES = CWD.joinpath('../../data/fake_data_structures')
PATH_TO_TEST_SUITES = CWD.joinpath('../../tests')


def create_model(llm=None):
    load_dotenv(find_dotenv())
    if llm is None:
        from langchain.chat_models import ChatOpenAI
        api_key = getenv('OPENAI_API_KEY')
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k",
                         openai_api_key=api_key, temperature=0)
    model = initialize_model(llm=llm, options={'memory': 3, 'review': True})
    return model


def get_sql_query(model, input):
    return model.predict(input)


def run_sample_in_terminal():
    """
    Creates a terminal instance
    1. Mimics the exact scenario in which the user will use this package
    """

    model = create_model()
    model.load_schema_from_file(CWD.joinpath(
        '../../data/schemas/website_aggregates.txt').absolute())

    while True:
        user_input = input("Enter something (or type 'exit' to close): ")
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'
        else:
            output = model.predict(user_input)
            if output.is_final_output:
                print("Query : \n\"", output.message + '"\n')
                print("Output : \n", execute_command(
                    output.message))
                print('-'*80 + '\n')
            else:
                print(output.message)


def run_test_suites():
    import pytest
    from InquirerPy import inquirer
    """
    This function should use the testcase_runner.py module to run the testcases

    This function should get inputs:
    1. List down all the test files for the user to select

    """

    test_files = glob(
        './**/*_test.py', root_dir=PATH_TO_TEST_SUITES.absolute())
    test_suite = inquirer.rawlist(
        message="Choose the Test file",
        choices=[
            re.sub(r'(^\./)', '', filename) for filename in test_files
        ]
    ).execute()

    complete_file_path = PATH_TO_TEST_SUITES.joinpath(test_suite).absolute()

    pytest.main(['-vv', '-s', complete_file_path,
                 '--maxfail='+str(sys.maxsize),
                 ])


def run_mock_data_generator():
    from .mock_data_generator import add_mock_data_to_db
    from InquirerPy import inquirer
    import importlib
    """
    This function should use the mock_data_generator.py module
    to create the mock data.

    The data structures will be listed under the file format
        <table_name>.py

    This function should get two inputs
    1. List down all the data structure files for the user to select
    2. Ask how many number of fake data has to be generated

    """
    fake_data_files = list(glob(
        './*.py', root_dir=PATH_TO_FAKE_DATASTRUCTURES.absolute()))
    fake_data_files.remove('./library.py')
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
        outputs = module.main()
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found.")

    for output in outputs:
        table_name = output.get('table_name', table_name)
        column_blueprint = output.get('column_blueprint')
        fake_data_structure = output.get('fake_data_structure')

        add_mock_data_to_db(table_name, column_blueprint,
                            fake_data_structure, num_of_fake_data_to_generate)
