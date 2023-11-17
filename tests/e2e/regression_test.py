import threading
import random
from tqdm import tqdm
from decimal import Decimal
from src import create_model
from src.database_connector import create_new_connection_and_execute
from decimal import Decimal
from pathlib import Path
from pytest_check import check

# Test Cases
testcases = [{
    'questions': [
        "How many total visitors have visited hardy.net domain?",
        "What is the total count of visitors who have accessed the hardy.net domain?",
        "Can you provide the aggregate number of visitors that have visited the hardy.net domain?",
        "How many visitors in total have accessed hardy.net?",
        "Give me the count of visitors that have accessed the hardy.net domain",
        "Could you tell me the number of people who visited the hardy.net domain?",
        "What's the cumulative count of visitors to the hardy.net domain?",
        "Tell me the information you have on the total visitors to hardy.net?",
        "Show me the visitor count for the hardy.net domain",
        "I'm curious about the total number of visitors who visited hardy.net. Can you provide that?",
        "What's the sum of visitors that have accessed hardy.net?",
        "Total Visitors of hardy.net",
        # # Phrases which are not directly requesting the visitor count
        # Not sure whether this phrasing is correct
        "What is the number of users visiting hardy.net domain",
        "Could you provide the statistics of user count for the hardy.net domain?",
        "What is the total number of users on hardy.net?",
        "I'm interested in the web activity metrics mainly the visitor count for specifically hardy.net. Could you share those?",
        "I'd like to know the number of users visited hardy.net. Can you retrieve that information?",
    ],
    'output': [(Decimal(4081),)],
    'sql_output': "SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'hardy.net';",
    'description': "Simple count of total visitors."
}, {
    'questions': [
        "How many total visitors have visited openai.com domain in the year 2023?",
        "Can you provide the total number of visitors who visited the openai.com domain throughout 2023?",
        "I'm curious about the total count of visitors that accessed the openai.com domain in the year 2023. Do you have that information?",
        "What's the overall visitor count for the openai.com domain specifically in the year 2023?",
        "Have you got data on the total number of people who visited openai.com during the entirety of 2023?",
        "Could you tell me the total visits registered for the openai.com domain in the calendar year of 2023?",
        "I'm interested in knowing the aggregate number of visitors who browsed the openai.com domain in 2023. Can you provide that?",
        "Is there information available regarding the total visitors who accessed openai.com in the year 2023?",
        "How many visitors accessed the openai.com domain during the entirety of 2023?",
        "Do you have data on the total number of individuals who visited openai.com in the year 2023?",
        "Can you fetch the total visits made to the openai.com domain over the course of 2023?",
        "Could you provide statistics on the total visits to the openai.com domain during 2023?",
        "I'm interested in knowing the count of total visitors specifically for the openai.com domain in the year 2023.",
        "Visitor Count for openai.com in 2023",  # How to assume openai as openai.com
        # # Phrases which are not directly requesting the visitor count
        "What's the total volume of visitors recorded for the openai.com website in the year 2023?",
        "What's the total footfall or visitor count for the openai.com domain throughout the year 2023?",
        "Is there information available on the number of overall visitors to the openai.com website throughout 2023?",
        "How many users visited openai.com in this year?"
    ],
    'output': [(Decimal(262354),)],
    'sql_output': """
    SELECT 
        SUM(no_of_visiting_ips) AS total_visitors
    FROM
        website_aggregates
    WHERE
        customer_domain = 'openai.com'
        AND dt >= '2023-01-01'
        AND dt <= '2023-12-31';
    """,
    'description': "Total count of visitors in the year 2023."
}, {
    'questions': [
        "How many total visitors have visited the lead domain lead domain tesla.com whose employee count is within 1000 to 10000?",
        "What's the total count of visitors to the lead domain tesla.com within the employee range of 1000 to 10000?",
        "Can you provide the overall number of visitors who have visited lead domain tesla.com who has the employee count between 1000 and 10000?",
        "How many visitors, specifically within the employee count of 1000 to 10000, have accessed the lead lead domain tesla.com?",
        "I'm interested in knowing the total visitor count to lead lead domain tesla.com with an employee range of 1000-10000. What is it?",
        "Could you tell me the total number of people who visited lead domain tesla.com considering an employee count between 1000 and 10000?",
        "What is the sum total of visitors that have accessed lead domain tesla.com within the 1000 to 10000 employee range?",
        "Do you have information on the total visitors to the lead domain tesla.com whose employee count falls between 1000 and 10000?",
        "I'm curious about the number of visitors who visited lead domain tesla.com with an employee count between 1000 and 10000. Can you provide that?",
        "What's the sum of total visitors that have accessed lead domain tesla.com considering the employee range of 1000 to 10000?",
        "Can you give me the total number of visitors to lead domain tesla.com where the employee count is between 1000 and 10000?",
        "How many total visits have occurred on lead domain tesla.com within the employee range of 1000-10000?",
        "What is the visitor count for lead domain tesla.com given an employee count between 1000 and 10000?",
        "I'd like to know the total number of visitors who have accessed lead domain tesla.com with an employee count within 1000 to 10000.",
        "What is the overall number of visitors to lead domain tesla.com with the employee range of 1000-10000?",
        "Could you provide insights into the total visitor count for lead domain tesla.com with total number of workers in thousand and ten thousands range?",
        "What's the cumulative number of visitors to lead domain tesla.com considering the employee count between 1000 and 10000?",
        "Show me the total visitors to lead domain tesla.com in the 1k to 10k employee range?",
        "What is the visitation count for lead domain tesla.com with the employee range of 1000 to 10000?",
        "I'd like to know the total visits to lead domain tesla.com when the employee count falls between 1000 and 10000."
        "Could you please share the number of visitors for lead domain tesla.com within the specified employee range of 1k to 10k?",
    ],
    'output': [(Decimal(290098),)],
    'sql_output': """
        SELECT
            SUM(no_of_visiting_ips) AS total_visitors
        FROM
            website_aggregates
        WHERE
            lead_domain = 'tesla.com'
            AND estimated_num_employees >= 1000
            AND estimated_num_employees <= 10000;
    """,
    'description': "Total count of visitors within a specified employee count range."
}, {
    'questions': [
        "How many total visitors have visited the lead domain meta.com whose revenue is between one hundred thousand and one million?",
        "What's the total count of visitors to lead domain meta.com within the revenue range of $100,000 to $1,000,000?",
        "Can you provide the overall number of visitors who have visited lead domain meta.com while having a revenue between $100,000 and $1,000,000?",
        "How many visitors, specifically within the revenue range of $100k-$1M, have accessed lead domain meta.com?",
        "I'm interested in knowing the total visitor count to lead domain meta.com with a revenue range of $100,000 - $1,000,000. What is it?",
        "Could you tell me the total number of people who visited lead domain meta.com considering a revenue between $100,000 and $1,000,000?",
        "What is the sum total of visitors that have accessed lead domain meta.com within the $100k-$1M revenue range?",
        "Do you have information on the total visitors to lead domain meta.com whose revenue falls between $100,000 and $1,000,000?",
        "Could you please share the total visitor count for lead domain meta.com within the revenue range of hundred thousand to 1 million?",
        "I'm curious about the number of visitors who visited lead domain meta.com with a revenue between $100,000 and $1,000,000. Can you provide that?",
        "What's the count of total visitors that have accessed lead domain meta.com considering the revenue range of $100k-$1M?",
        "Can you give me the total number of visitors to lead domain meta.com where the revenue is between $100,000 and $1,000,000?",
        "How many total visits have occurred on lead domain meta.com within the revenue range of $100k-$1M?",
        "What is the visitor count for lead domain meta.com given a revenue range between $100,000 and $1,000,000?",
        "I'd like to know the total number of visitors who have accessed lead domain meta.com with a revenue within $100,000 to $1,000,000.",
        "What is the overall number of visitors to lead domain meta.com with the revenue range of $100k-$1M?",
        "What's the cumulative number of visitors to lead domain meta.com considering the revenue between $100,000 and $1,000,000?",
        "What is the visiting count for lead domain meta.com with the revenue range of $100,000 to $1,000,000?",
        "I'd like to know the total visits to lead domain meta.com when the revenue falls between $100,000 and $1,000,000."
    ],
    'output': [(Decimal(290889),)],
    'sql_output': """
            SELECT
                SUM(no_of_visiting_ips) AS total_visitors
            FROM
                website_aggregates
            WHERE
                lead_domain = 'meta.com'
                AND annual_revenue >= 100000
                AND annual_revenue <= 1000000;
        """,
    'description': "Total count of visitors within a specified revenue range."
}]

# Helper Functions


def linearize_testcases(testcases):
    array = []
    for testcase in testcases:
        questions = testcase['questions']
        output = testcase['output']
        sql_output = testcase['sql_output']
        for question in questions:
            array.append({
                'input': question,
                'output': output,
                'sql_output': sql_output
            })

    random.shuffle(array)
    return array


def check_value(value, expected, info=''):
    with check:
        assert expected == value, info


def run_model(testcase):
    model = create_model()
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

    for i in range(NO_OF_REPETITIONS):
        user_input = testcase['input']
        expected_output = testcase['output']
        expected_sql_output = testcase['sql_output']
        llm_response = model.predict(user_input)
        model_sql_output = llm_response.message
        is_final_output = llm_response.is_final_output
        check_value(
            is_final_output,
            True,
            'Model isn\'t able to predict the response in single shot'
        )
        if is_final_output:
            model_output = create_new_connection_and_execute(model_sql_output)
            debugging_info = f"\
            \nUser Chat = {user_input}\
            \nProper SQL Query = {expected_sql_output}\
            \nActual SQL Query = {model_sql_output}\
            \nSQL Output = {model_output}\
            "
            check_value(model_output, expected_output, f'{debugging_info}')

        progress_bar.update(NO_OF_ASSERTIONS_PER_TEST)


CWD = Path(__file__).parent

testcases = linearize_testcases(testcases[:])

NO_OF_REPETITIONS = 1
NO_OF_ASSERTIONS_PER_TEST = 2

progress_bar = tqdm(total=len(testcases) *
                    NO_OF_REPETITIONS * NO_OF_ASSERTIONS_PER_TEST)

# Entry Point for PyTest


def test_accuracy_of_model():
    threads = []
    for testcase in testcases:
        threads.append(
            threading.Thread(
                target=run_model,
                args=[testcase]
            )
        )

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    # print(execute_command("""
    #     SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'hardy.net';
    # """))
    # test_accuracy_of_model()
    pass
