"""
Here the testcases for the function has to be added
This testcases should follow a format

[{
    input : '...' -> Input from user,
    sql_output : '...' -> SQL output,
    description : '...' -> Any Description (Optional)
}]
"""

from src import create_model
from src.database_connector import execute_command
from pathlib import Path

CWD = Path(__file__).parent

testcases = [
    {
        'input': "How many total visitors have visited hardy.net domain?",
        'sql_output': "SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'hardy.net';",
        'description': "Simple count of total visitors."
    },
    {
        'input': "How many total visitors have visited google.com domain in the last 7 days?",
        'sql_output': "SELECT SUM(no_of_visiting_ips) AS total_visitors FROM website_aggregates WHERE customer_domain = 'google.com' AND dt >= current_date - INTERVAL '7 days';",
        'description': "Total count of visitors in the last 7 days."
    },

    {
        'input': "How many total visitors have visited openai.com domain in the year 2023?",
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
        "input": "What is the total number of hits for google.com in February 2023?",
        "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE customer_domain = 'google.com' AND dt BETWEEN '2023-02-01' AND '2023-02-28';",
        "description": "Calculates the total number of hits for google.com in February 2023."
    },
    {
        "input": "Can you show the total annual revenue for all customers in the hospitality industry?",
        "sql_output": "SELECT SUM(annual_revenue) FROM website_aggregates WHERE industry = 'hospitality';",
        "description": "Summarizes the total annual revenue for customers in the hospitality industry."
    },
    {
        "input": "How many unique IPs visited fb.com from India in March 2023?",
        "sql_output": "SELECT SUM(DISTINCT no_of_visiting_ips) FROM website_aggregates WHERE customer_domain = 'fb.com' AND ip_country = 'India' AND dt BETWEEN '2023-03-01' AND '2023-03-31';",
        "description": "Counts the unique IPs that visited fb.com from India in March 2023."
    },
    {
        "input": "What was the total funding for companies in the investment management industry last year?",
        "sql_output": "SELECT SUM(total_funding) FROM website_aggregates WHERE industry = 'investment management' AND dt BETWEEN '2022-01-01' AND '2022-12-31';",
        "description": "Calculates the total funding for companies in the investment management industry in the previous year."
    },
    {
        "input": "How many leads were qualified from the state of Michigan in April 2023?",
        "sql_output": "SELECT COUNT(*) FROM website_aggregates WHERE state = 'Michigan' AND status = 'Qualified' AND dt BETWEEN '2023-04-01' AND '2023-04-30';",
        "description": "Counts the number of qualified leads from Michigan in April 2023."
    },
    {
        "input": "What is the average number of hits per day for amazon.com in May 2023?",
        "sql_output": "SELECT AVG(no_of_hits) FROM website_aggregates WHERE customer_domain = 'amazon.com' AND dt BETWEEN '2023-05-01' AND '2023-05-31';",
        "description": "Calculates the average number of hits per day for amazon.com in May 2023."
    },
    {
        "input": "What is the total number of employees across all customer domains in the healthcare industry?",
        "sql_output": "SELECT SUM(estimated_num_employees) FROM website_aggregates WHERE industry = 'healthcare';",
        "description": "Summarizes the total number of employees across all customer domains in the healthcare industry."
    },
    {
        "input": "How many customers have an annual revenue of over $1 million in the retail sector?",
        "sql_output": "SELECT COUNT(*) FROM website_aggregates WHERE annual_revenue > 1000000 AND industry = 'retail';",
        "description": "Counts the number of customers in the retail sector with an annual revenue of over $1 million."
    },
    {
        "input": "What was the latest funding stage for leads in the automotive industry in September 2023?",
        "sql_output": "SELECT latest_funding_stage FROM website_aggregates WHERE industry = 'automotive' AND dt BETWEEN '2023-09-01' AND '2023-09-30' ORDER BY dt DESC LIMIT 1;",
        "description": "Finds the most recent funding stage for leads in the automotive industry in September 2023."
    },
    {
        "input": "Can you list the total number of hits for each customer domain in October 2023?",
        "sql_output": "SELECT customer_domain, SUM(no_of_hits) FROM website_aggregates WHERE dt BETWEEN '2023-10-01' AND '2023-10-31' GROUP BY customer_domain;",
        "description": "Lists the total number of hits for each customer domain in October 2023."
    },
    {
        "input": "How many visiting IPs were from Canada to microsoft.com in November 2023?",
        "sql_output": "SELECT SUM(no_of_visiting_ips) FROM website_aggregates WHERE customer_domain = 'microsoft.com' AND ip_country = 'Canada' AND dt BETWEEN '2023-11-01' AND '2023-11-30';",
        "description": "Counts the number of visiting IPs from Canada to microsoft.com in November 2023."
    },
    {
        "input": "What is the estimated number of employees for leads from New York in December 2023?",
        "sql_output": "SELECT estimated_num_employees FROM website_aggregates WHERE state = 'New York' AND dt BETWEEN '2023-12-01' AND '2023-12-31';",
        "description": "Calculates the total estimated number of employees for leads from New York in December 2023."
    },
    {
        "input": "How many disqualified leads were there from the pharmaceutical industry last year?",
        "sql_output": "SELECT COUNT(*) FROM website_aggregates WHERE industry = 'pharmaceutical' AND status = 'Disqualified' AND dt BETWEEN '2022-01-01' AND '2022-12-31';",
        "description": "Counts the number of disqualified leads from the pharmaceutical industry in the previous year."
    },
    {
        "input": "What is the average annual revenue for companies in the '251 - 500' employee range?",
        "sql_output": "SELECT AVG(annual_revenue) FROM website_aggregates WHERE employee_range = '251 - 500';",
        "description": "Calculates the average annual revenue for companies with 251 - 500 employees."
    },
    {
        "input": "How many visits were made to companies in the '10M - 100M' revenue range in February 2024?",
        "sql_output": "SELECT SUM(no_of_visiting_ips) AS total_visits FROM website_aggregates WHERE revenue_range = '10M - 100M' AND dt BETWEEN '2024-02-01' AND '2024-02-28';",
        "description": "Counts the number of visits by companies in the '10M - 100M' revenue range in February 2024."
    },
    {
        "input": "What is the count of unique visiting IPs to apple.com from Australia in March 2024?",
        "sql_output": "SELECT SUM(DISTINCT no_of_visiting_ips) FROM website_aggregates WHERE customer_domain = 'apple.com' AND ip_country = 'Australia' AND dt BETWEEN '2024-03-01' AND '2024-03-31';",
        "description": "Counts the unique visiting IPs to apple.com from Australia in March 2024."
    },
    {
        "input": "How many total hits did facebook.com have from Germany in April 2024?",
        "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE customer_domain = 'facebook.com' AND ip_country = 'Germany' AND dt BETWEEN '2024-04-01' AND '2024-04-30';",
        "description": "Calculates the total number of hits that facebook.com received from Germany in April 2024."
    },
    {
        "input": "What is the total number of companies with less than 100 employees in the finance sector?",
        "sql_output": "SELECT COUNT(DISTINCT customer_domain) FROM website_aggregates WHERE industry = 'finance' AND estimated_num_employees < 100;",
        "description": "Counts the total number of companies with less than 100 employees in the finance sector."
    },
    {
        "input": "What was the total funding received by companies in the media sector last quarter?",
        "sql_output": "SELECT SUM(total_funding) FROM website_aggregates WHERE industry = 'media' AND dt BETWEEN (CURRENT_DATE - INTERVAL '3 months') AND CURRENT_DATE;",
        "description": "Calculates the total funding received by companies in the media sector in the last quarter."
    },
    {
        "input": "How many site visits were made by companies from Japan in July 2024?",
        "sql_output": "SELECT SUM(no_of_visiting_ips) FROM website_aggregates WHERE company_country = 'Japan' AND dt BETWEEN '2024-07-01' AND '2024-07-31';",
        "description": "Counts the number of site visits made by companies from Japan in July 2024."
    },
    {
        "input": "Can you show the number of hits for each lead domain in the energy sector in August 2024?",
        "sql_output": "SELECT lead_domain, SUM(no_of_hits) FROM website_aggregates WHERE industry = 'energy' AND dt BETWEEN '2024-08-01' AND '2024-08-31' GROUP BY lead_domain;",
        "description": "Lists the total number of hits for each lead domain in the energy sector in August 2024."
    },
    {
        "input": "What is the total number of employees for all leads in the manufacturing industry?",
        "sql_output": "SELECT SUM(estimated_num_employees) FROM website_aggregates WHERE industry = 'manufacturing';",
        "description": "Calculates the total number of employees for all leads in the manufacturing industry."
    },
    {
        "input": "What is the total annual revenue for customer domains in the legal sector?",
        "sql_output": "SELECT SUM(annual_revenue) FROM website_aggregates WHERE industry = 'legal';",
        "description": "Calculates the total annual revenue for customer domains in the legal sector."
    },
    {
        "input": "How many unique IPs visited netflix.com from Brazil in October 2024?",
        "sql_output": "SELECT COUNT(DISTINCT no_of_visiting_ips) FROM website_aggregates WHERE customer_domain = 'netflix.com' AND ip_country = 'Brazil' AND dt BETWEEN '2024-10-01' AND '2024-10-31';",
        "description": "Counts the number of unique IPs that visited netflix.com from Brazil in October 2024."
    },
    {
        "input": "What is the total number of hits for companies in the 'Seed' funding stage in November 2024?",
        "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE latest_funding_stage = 'Seed' AND dt BETWEEN '2024-11-01' AND '2024-11-30';",
        "description": "Calculates the total number of hits for companies in the 'Seed' funding stage in November 2024."
    },
    {
        "input": "What was the last visit date for leads from the advertising industry last month?",
        "sql_output": "SELECT MAX(last_visit_date) FROM website_aggregates WHERE industry = 'advertising' AND dt BETWEEN (CURRENT_DATE - INTERVAL '1 month') AND CURRENT_DATE;",
        "description": "Finds the last visit date for leads from the advertising industry in the previous month."
    },
    {
        "input": "How many total hits did twitter.com have from South Africa last year?",
        "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE customer_domain = 'twitter.com' AND ip_country = 'South Africa' AND dt BETWEEN '2023-01-01' AND '2023-12-31';",
        "description": "Summarizes the total hits that twitter.com received from South Africa in the last year."
    },
    {
        "input": "Can you provide the average number of site visits per company in the 'Real Estate' sector?",
        "sql_output": "SELECT AVG(no_of_visiting_ips) FROM website_aggregates WHERE industry = 'Real Estate';",
        "description": "Calculates the average number of site visits per company in the Real Estate sector."
    },
    {
        "input": "What is the total number of employees for customer domains from Texas?",
        "sql_output": "SELECT SUM(estimated_num_employees) FROM website_aggregates WHERE state = 'Texas';",
        "description": "Calculates the total number of employees for customer domains from Texas."
    },
    {
        "input": "How many unique IPs visited linkedin.com from the UK in the last six months?",
        "sql_output": "SELECT COUNT(DISTINCT no_of_visiting_ips) FROM website_aggregates WHERE customer_domain = 'linkedin.com' AND ip_country = 'United Kingdom' AND dt BETWEEN (CURRENT_DATE - INTERVAL '6 months') AND CURRENT_DATE;",
        "description": "Counts the number of unique IPs that visited linkedin.com from the UK in the last six months."
    },
    {
        "input": "Can you show the total funding received by companies in the 'Biotechnology' sector?",
        "sql_output": "SELECT SUM(total_funding) FROM website_aggregates WHERE industry = 'Biotechnology';",
        "description": "Shows the total funding received by companies in the Biotechnology sector."
    },
    {
        "input": "What is the average annual revenue for leads in the '1001 - 5000' employee range?",
        "sql_output": "SELECT AVG(annual_revenue) FROM website_aggregates WHERE employee_range = '1001 - 5000';",
        "description": "Calculates the average annual revenue for leads with 1001 - 5000 employees."
    },
    {
        "input": "What was the total number of hits for all customer domains in the 'Logistics' industry?",
        "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE industry = 'Logistics';",
        "description": "Summarizes the total number of hits for all customer domains in the Logistics industry."
    },
    {
        "input": "What is the total number of site visits from companies in the '1M - 10M' revenue range?",
        "sql_output": "SELECT SUM(no_of_visiting_ips) FROM website_aggregates WHERE revenue_range = '1M - 10M';",
        "description": "Calculates the total number of site visits from companies in the '1M - 10M' revenue range."
    },
    {
        "input": "What is the total number of hits for spotify.com from Canada last year?",
        "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE customer_domain = 'spotify.com' AND ip_country = 'Canada' AND dt BETWEEN '2022-01-01' AND '2022-12-31';",
        "description": "Calculates the total number of hits for spotify.com from Canada in the last year."
    },
    {
        "input": "Can you show the number of qualified leads from the 'Telecommunications' industry?",
        "sql_output": "SELECT COUNT(*) FROM website_aggregates WHERE industry = 'Telecommunications' AND status = 'Qualified';",
        "description": "Shows the number of qualified leads from the Telecommunications industry."
    },
    {
        "input": "What is the total number of employees for leads in the 'Government' sector?",
        "sql_output": "SELECT SUM(estimated_num_employees) FROM website_aggregates WHERE industry = 'Government';",
        "description": "Calculates the total number of employees for leads in the Government sector."
    },
    {
        "input": "Can you list the total number of hits for each customer domain in the 'Construction' sector?",
        "sql_output": "SELECT customer_domain, SUM(no_of_hits) FROM website_aggregates WHERE industry = 'Construction' GROUP BY customer_domain;",
        "description": "Lists the total number of hits for each customer domain in the Construction sector."
    },
    {
        "input": "What is the average number of site visits per day for companies in the 'E-commerce' sector?",
        "sql_output": "SELECT AVG(no_of_visiting_ips) FROM website_aggregates WHERE industry = 'E-commerce';",
        "description": "Calculates the average number of site visits per day for companies in the E-commerce sector."
    }
]


def check(value, expected, info=''):
    assert value == expected, info


def test_accuracy():
    model = create_model()
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

    for testcase in testcases:
        user_input = testcase['input']
        expected_sql_output = testcase['sql_output']
        llm_response = model.predict(user_input)
        model_sql_output = llm_response.message
        is_final_output = llm_response.is_final_output
        check(is_final_output, True, testcase['description'] if 'description' in testcase else "No Problem Description Provided:" + testcase['input'])
        model_output = execute_command(model_sql_output)
        expected_output = execute_command(expected_sql_output)
        debugging_info = f'{expected_sql_output=}, {model_sql_output=}, {testcase["description"] if "description" in testcase else "No Problem Description Provided"}'
        check(model_output, expected_output, f'{debugging_info}')