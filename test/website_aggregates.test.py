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

test_cases = [
    {
        'input': "How many total visitors have visited this domain?",
        'output': "7105",
        'sql_output': "SELECT COUNT(*) FROM visitors;",
        'description': "Simple count of total visitors."
    },
    {
        'input': "How many total visitors have visited this domain in the last 7 days?",
        'output': "Visitors in the last 7 days: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE visit_date >= current_date - INTERVAL '7 days';",
        'description': "Count of visitors in the last 7 days."
    },
    {
        'input': "How many total visitors have visited this domain in the year 2022?",
        'output': "Visitors in 2022: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE EXTRACT(YEAR FROM visit_date) = 2022;",
        'description': "Count of visitors in the year 2022."
    },
    {
        'input': "How many total visitors have visited this domain whose employee count is within a given range?",
        'output': "Visitors within the specified employee count range: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE employee_count >= <min_count> AND employee_count <= <max_count>;",
        'description': "Count of visitors within a specified employee count range."
    },
    {
        'input': "How many total visitors have visited this domain whose revenue range is within a given range?",
        'output': "Visitors within the specified revenue range: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE revenue >= <min_revenue> AND revenue <= <max_revenue>;",
        'description': "Count of visitors within a specified revenue range."
    },
    {
        'input': "How many total visitors have visited this domain from the country United States?",
        'output': "Visitors from United States: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE country = 'United States';",
        'description': "Count of visitors from a specific country."
    },
    {
        'input': "How many total visitors have visited this domain whose revenue range is within a given range, whose employee count range is within a given range and whose last_visit_date is <date>?",
        'output': "Visitors meeting all specified criteria: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE revenue >= <min_revenue> AND revenue <= <max_revenue> AND employee_count >= <min_employee_count> AND employee_count <= <max_employee_count> AND last_visit_date = '<date>';",
        'description': "Count of visitors meeting multiple criteria."
    },
    {
        'input': "How many total visitors have visited this domain whose employee count is within this count range?",
        'output': "Visitors within the specified employee count range: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE employee_count >= <min_count> AND employee_count <= <max_count>;",
        'description': "Count of visitors within a specified employee count range."
    },
    {
        'input': "How many total visitors have visited this domain whose industry is Technology?",
        'output': "Visitors in the Technology industry: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE industry = 'Technology';",
        'description': "Count of visitors in a specific industry."
    },
    {
        'input': "How many <insert some measure> have visited this domain whose <some other condition>?",
        'output': "<Some measure> meeting the specified condition: <number>",
        'sql_output': "SELECT COUNT(*) FROM visitors WHERE <some_other_condition>;",
        'description': "Count of a specific measure meeting a condition."
    },
]
