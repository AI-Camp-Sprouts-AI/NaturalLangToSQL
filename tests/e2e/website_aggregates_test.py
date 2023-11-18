import threading
import random
import time
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
}, {
    "questions": [
        "What is the total count of visitors who visited the alphabet.com domain from the US?",
        "From the US, how many total visitors have accessed the alphabet.com domain?",
        "Count the total number of visitors from the US to alphabet.com.",
        "Could you tell me the total visitors from the US that visited alphabet.com?",
        "I'm interested in knowing the total count of visitors from the US who visited alphabet.com. Could you provide that?",
        "What's the total number of visitors from the US that accessed the alphabet.com domain?",
        "How many visitors, in total, visited alphabet.com from the US?",
        "From the US, what's the total count of visitors to the alphabet.com domain?",
        "Provide the total count of visitors from the US who accessed alphabet.com, please.",
        "Tell me the overall number of visitors from the US who visited the alphabet.com domain.",
        "What's the total visitor count from the US that accessed alphabet.com?",
        "I'd like to know the total number of visitors from the United States who visited alphabet.com.",
        "Could you give me the total count of visitors who visited alphabet.com from the US?",
        "Provide the total count of visitors who accessed the alphabet.com domain from the United States.",
        "How many visitors from the United States visited the alphabet.com domain in total?",
        "What's the total number of visitors who visited alphabet.com from the US?",
        "I'm curious about the total count of visitors from the United States who accessed alphabet.com.",
        "From the US, what is the total number of visitors to the alphabet.com domain?",
        "Could you share the total number of visitors from the United States who visited alphabet.com?",
        "What is the total count of visitors from the United States that accessed alphabet.com?"
    ],
    'output': [(Decimal(13542),)],
    'sql_output': """
            SELECT
                SUM(no_of_visiting_ips) AS total_visitors
            FROM
                website_aggregates
            WHERE
                customer_domain = 'alphabet.com'
                AND ip_country = 'United States'
        """,
    'description': "Total count of visitors from a specific country."
}, {
    'questions': [
        "How many total visitors have visited alphabet.com domain whose employee count is within 3000 to 5000 count range?"
        "What is the total count of visitors who visited alphabet.com domain within the employee count range of 3000 to 5000?",
        "How many visitors, in total, visited alphabet.com within the range of 3000 to 5000 employees?",
        "Count the total number of visitors who visited alphabet.com within the 3000 to 5000 employee count range.",
        "Could you tell me the total visitors who visited alphabet.com with an employee count between 3000 and 5000?",
        "I'm interested in knowing the total count of visitors to alphabet.com within the employee count range of 3000 to 5000. Can you provide that?",
        "What's the total number of visitors who visited alphabet.com within the range of 3000 to 5000 employees?",
        "How many visitors, in total, visited alphabet.com with an employee count between 3000 and 5000?",
        "Provide the total count of visitors who visited alphabet.com within the employee count range of 3000 to 5000, please.",
        "Tell me the overall number of visitors who visited alphabet.com within the 3000 to 5000 employee count range.",
        "What's the total visitor count to alphabet.com within the range of 3000 to 5000 employees?",
        "I'd like to know the total number of visitors who visited alphabet.com within the employee count range of 3000 to 5000.",
        "Could you give me the total count of visitors who visited alphabet.com within the 3000 to 5000 employee count range?",
        "Provide the total count of visitors who visited alphabet.com within the range of 3000 to 5000 employees.",
        "How many visitors visited the alphabet.com domain with an employee count between 3000 and 5000 in total?",
        "What's the total number of visitors who visited alphabet.com within the 3000 to 5000 employee count range?",
        "I'm curious about the total count of visitors who visited alphabet.com within the 3000 to 5000 employee count range.",
        "What is the total count of visitors who visited alphabet.com within the employee count range of 3000 to 5000?",
        "Could you share the total number of visitors who visited alphabet.com within the 3000 to 5000 employee count range?",
        "Tell me the count of visitors from the alphabet.com domain within the 3000 to 5000 employee count range.",
        "What is the total count of visitors who visited alphabet.com within the 3000 to 5000 employee count range?"
    ],
    'output': [(Decimal(60770),)],
    'sql_output': """
            SELECT SUM(no_of_visiting_ips) AS total_visitors
            FROM website_aggregates
            WHERE customer_domain = 'alphabet.com'
            AND estimated_num_employees >= 3000
            AND estimated_num_employees <= 5000;
        """,
    'description': "Total count of visitors within a specified employee count range."
}, {
    "questions": [
        "What is the total count of visitors from the energy field who have visited apple.com domain?",
        "How many visitors, in total, from the energy sector have visited apple.com?",
        "Count the total number of visitors from the energy field who visited apple.com.",
        "Could you tell me the total visitors from the energy field who have visited apple.com?",
        "I'm interested in knowing the total count of visitors from the energy sector who visited apple.com. Can you provide that?",
        "What's the total number of visitors from the energy field who have visited apple.com?",
        "How many visitors, in total, visited apple.com from the energy field?",
        "Provide the total count of visitors from the energy sector who visited apple.com, please.",
        "Tell me the overall number of visitors from the energy field who visited apple.com.",
        "What's the total visitor count from the energy field who visited apple.com?",
        "I'd like to know the total number of visitors from the energy sector who visited apple.com.",
        "Could you give me the total count of visitors from the energy field who have visited apple.com?",
        "Provide the total count of visitors who visited apple.com from the energy field.",
        "How many visitors from the energy field visited the apple.com domain in total?",
        "What's the total number of visitors from the energy field who have visited apple.com?",
        "I'm curious about the total count of visitors from the energy field who visited apple.com.",
        "What is the total count of visitors from the energy field who have visited apple.com?",
        "Could you share the total number of visitors from the energy sector who visited apple.com?",
        "Tell me the count of visitors from the energy field who have visited apple.com.",
        "What is the total count of visitors from the energy field who visited apple.com?"
    ],
    'output': [(Decimal(12235),)],
    'sql_output': """
            SELECT SUM(no_of_visiting_ips) AS total_visitors
            FROM website_aggregates
            WHERE customer_domain = 'apple.com'
            AND industry = 'energy';
        """,
    'description': "Total count of visitors in a specific industry."
}]

# Helper Functions


def linearize_testcases(testcases, no_of_repetitions=1):
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
    array *= no_of_repetitions
    random.shuffle(array)
    return array


def split_into_batches(array, count=100):
    batches = []
    i = 0
    while i < len(array):
        batches.append(array[i:i+count])
        i += count

    return batches


def check_value(value, expected, info=''):
    with check:
        assert expected == value, info


def run_model(testcase):
    model = create_model()
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

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
NO_OF_REPETITIONS = 1
NO_OF_ASSERTIONS_PER_TEST = 2

testcases = linearize_testcases(testcases[:], NO_OF_REPETITIONS)


progress_bar = tqdm(total=len(testcases) * NO_OF_ASSERTIONS_PER_TEST,
                    desc='Assertions Completed')

# Entry Point for PyTest


def test_accuracy_of_model():
    batches = split_into_batches(testcases, count=100)
    batches_progress = tqdm(total=len(batches)+1, desc='Batches Completed')
    for set_of_testcases in batches:
        threads = []
        for testcase in set_of_testcases:
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
        batches_progress.update(1)
        time.sleep(0.5)


if __name__ == '__main__':
    # print(execute_command("""
    #     SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'hardy.net';
    # """))
    # test_accuracy_of_model()
    pass
