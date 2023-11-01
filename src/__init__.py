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
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",
                     openai_api_key=api_key, temperature=0)
    model = initialize_model(llm=llm, options={'memory': 3})
    model.load_schema_as_string("""
    CREATE TABLE WebsiteAggregates (
        dt DATE,
        customer_domain VARCHAR(255),
        lead_domain VARCHAR(255),
        ip_country VARCHAR(255),
        no_of_visiting_ips BIGINT,
        no_of_hits BIGINT,
        lead_domain_name VARCHAR(255),
        industry VARCHAR(255),
        estimated_num_employees INT,
        city VARCHAR(255),
        state VARCHAR(255),
        company_country VARCHAR(255),
        annual_revenue FLOAT,
        total_funding FLOAT,
        latest_funding_stage VARCHAR(255),
        status VARCHAR(255),
        decayed_inbound_score DOUBLE,
        decayed_intent_score DOUBLE,
        decayed_clubbed_score DOUBLE,
        last_visit_date DATE,
        employee_range VARCHAR(255),
        revenue_range VARCHAR(255)
    );""")

    while True:
        user_input = input("Enter something (or type 'exit' to close): ")
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'
        else:
            output = model.predict(user_input)
            print(output.message + '\n')


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
    print("Create the mock data here...")
    # Call the mock_data_generator file here
