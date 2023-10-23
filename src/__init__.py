from .main import initialize_model
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from os import getenv

def create_terminal_instance():
    """
    Creates a terminal instance
    1. Mimics the exact scenario in which the user will use this package
    """
    print("Creating a Terminal Instance for testing in dev environment...")

    load_dotenv()
    api_key = getenv('OPENAI_API_KEY')
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=api_key, temperature=0)
    model = initialize_model(llm=llm, options={'memory': 3})
    model.load_schema_as_string("""
        CREATE TABLE domains (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL
        );
        CREATE TABLE visitors (
            id INT PRIMARY KEY AUTO_INCREMENT,
            domain_id INT,
            visit_date DATE,
            country VARCHAR(100),
            employee_count INT,
            revenue DECIMAL(20, 2),
            industry VARCHAR(255),
            FOREIGN KEY (domain_id) REFERENCES domains(id)
        );""")

    while True:
        user_input = input("Enter something (or type 'exit' to close): ")
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'
        else:
            output = model.predict(user_input)
            print(output.message + '\n')


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
    print("Create the mock data here...")
    # Call the mock_data_generator file here