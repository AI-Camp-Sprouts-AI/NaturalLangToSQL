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

​


Note: This is not an exhaustive list of all the queries, if you feel there might be some more type of queries, add those too.
"""

test_cases = [
    {
        'input': "How many total visitors have visited this domain?",
        'output': "Total visitors: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates;",
        'description': "Total count of total visitors."
    },
    {
        'input': "How many total visitors have visited this domain in the last 7 days?",
        'output': "Visitors in the last 7 days: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ups) FROM website aggregates WHERE dt >= current_date - INTERVAL '7 days';",
        'description': "Total count of visitors in the last 7 days."
    },
    {
        'input': "How many total visitors have visited this domain in the year 2022?",
        'output': "Visitors in 2022: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE EXTRACT(YEAR FROM dt) = 2022;",
        'description': "Total count of visitors in the year 2022."
    },
    {
        'input': "How many total visitors have visited this domain whose employee count is within a given range?",
        'output': "Visitors within the specified employee count range: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE estimated_num_employees BETWEEN <min_count> AND <max_count>;",
        'description': "Total count of visitors within a specified employee count range."
    },
    {
        'input': "How many total visitors have visited this domain whose revenue range is within a given range?",
        'output': "Visitors within the specified revenue range: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE revenue_range BETWEEN <min_revenue> AND <max_revenue>;",
        'description': "Total count of visitors within a specified revenue range."
    },
    {
        'input': "How many total visitors have visited this domain from the country United States?",
        'output': "Visitors from United States: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE ip_country = 'United States';",
        'description': "Total count of visitors from a specific country."
    },
    {
        'input': "How many total visitors have visited this domain whose revenue range is within a given range, whose employee count range is within a given range and whose last_visit_date is <date>?",
        'output': "Visitors meeting all specified criteria: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE revenue BETWEEN <min_revenue> AND <max_revenue> AND employee_count BETWEEN <min_employee_count> AND <max_employee_count> AND last_visit_date = '<date>';",
        'description': "Total count of visitors meeting multiple criteria."
    },
    {
        'input': "How many total visitors have visited this domain whose employee count is within this count range?",
        'output': "Visitors within the specified employee count range: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE employee_count >= <min_count> AND employee_count <= <max_count>;",
        'description': "Total count of visitors within a specified employee count range."
    },
    {
        'input': "How many total visitors have visited this domain whose industry is Technology?",
        'output': "Visitors in the Technology industry: <number>",
        'sql_output': "SELECT SUM(no_of_visiting_ips) FROM website aggregates WHERE industry = 'Technology';",
        'description': "Total count of visitors in a specific industry."
    },
    {
        'input': "How many <measure> have visited this domain whose <condition>?",
        'output': "<Some measure> meeting the specified condition: <number>",
        'sql_output': "SELECT SUM(<measure>) FROM website aggregates WHERE <condition>;",
        'description': "Total count of a specific measure meeting a condition."
    },
]