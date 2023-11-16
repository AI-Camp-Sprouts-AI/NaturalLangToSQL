"""
Here the testcases for the function has to be added

This testcases should follow a format

[{
    input : '...' -> Input from user,
    output : '...' -> Output from the model, 
    sql_output : '...' -> SQL output,
    description : '...' -> Any Description (Optional)
}]


Natural Language Inputs:
-- How many total visitors have visited this domain?
-- How many total visitors have visited this domain in the last 7 days?
-- How many total visitors have visited this domain in the year 2022? 
-- How many total visitors have visited this domain whose employee count is within <a given range > ? 
-- How many total visitors have visited this domain whose revenue range is within <a given range > ? 
-- How many total visitors have visited this domain from the country <insert country here> ? 
-- How many total visitors have visited this domain whose revenue range is within <a given range >, whose employee count range is within <a given range> and whose last_visit_date is <date> ? 
-- How many total visitors have visited this domain whose employee count is within < this count range > ? 
-- How many total visitors have visited this domain whose industry is <insert industry> ? 
-- How many <insert some measure> have visited this domain whose <some other condition> ? 



Note: This is not an exhaustive list of all the queries, if you feel there might be some more type of queries, add those too.
"""

from src import create_model
from src.database_connector import execute_command
from decimal import Decimal
from pathlib import Path
from pytest_check import check

CWD = Path(__file__).parent

testcases = [
    {
        'input': "How many total visitors have visited hardy.net domain?",
        'output': [(Decimal(4081),)],
        'sql_output': "SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'hardy.net';",
        'description': "Simple count of total visitors."
    },
    # # Flaky Test as it tests last 7 days -> the output is dependent on current date
    # {
    #     'input': "How many total visitors have visited google.com domain in the last 7 days?",
    #     'output': [(Decimal(40398),)],
    #     'sql_output': "SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'google.com' AND dt >= current_date - INTERVAL '7 days';",
    #     'description': "Total count of visitors in the last 7 days."
    # },
    {
        'input': "How many total visitors have visited openai.com domain in the year 2023?",
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
        'description': "Total count of visitors in the year 2022."
    },
    {
        'input': "How many total visitors have visited the lead tesla.com whose employee count is within 1000 to 10000?",
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
    },
    {
        'input': "How many total visitors have visited the lead meta.com whose revenue is between one hundred thousand and one million?",
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
    },
    {
        'input': "How many total visitors have visited alphabet.com domain from US?",
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
    },
    {
        'input': "How many total visitors have visited alphabet.com domain whose employee count is within 3000 to 5000 count range?",
        'output': [(Decimal(60770),)],
        'sql_output': """
            SELECT SUM(no_of_visiting_ips) AS total_visitors
            FROM website_aggregates
            WHERE customer_domain = 'alphabet.com'
            AND estimated_num_employees >= 3000
            AND estimated_num_employees <= 5000;
        """,
        'description': "Total count of visitors within a specified employee count range."
    },
    {
        'input': "How many total visitors have visited apple.com domain who are from energy field?",
        'output': [(Decimal(12235),)],
        'sql_output': """
            SELECT SUM(no_of_visiting_ips) AS total_visitors
            FROM website_aggregates
            WHERE customer_domain = 'apple.com'
            AND industry = 'energy';
        """,
        'description': "Total count of visitors in a specific industry."
    }
]


def check_value(value, expected, info=''):
    with check:
        assert expected == value, info


def test_accuracy():
    model = create_model()
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

    for testcase in testcases:
        for i in range(1):
            user_input = testcase['input']
            expected_output = testcase['output']
            expected_sql_output = testcase['sql_output']
            llm_response = model.predict(user_input)
            model_sql_output = llm_response.message.replace('\n', ' ')
            is_final_output = llm_response.is_final_output
            # check_value(
            #     is_final_output, 
            #     True, 
            #     'Model isn\'t able to predict the response in single shot'
            # )
            model_output = execute_command(model_sql_output)
            debugging_info = f"""
            User Chat = {user_input}
            Expected SQL Output = {expected_sql_output}
            AI\' SQL Output = {model_sql_output}
            """
            check_value(model_output, expected_output, f'{debugging_info}')