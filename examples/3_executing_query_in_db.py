import os
from text_to_sql import create_model, \
    get_sql_query, \
    execute_command, \
    connect_and_execute_command
from pathlib import Path
"""
Load Schema from file and hit the query in mock database
"""
# !IMPORTANT: OPENAI_API_KEY should be added in the environment variable before calling this function
model = create_model()

cwd = Path(__file__).parent

query = input('Enter your question here: ')

model.load_schema_from_file(cwd.joinpath('./schema.txt').absolute())

output = get_sql_query(model, query)

sql_query = output.message

print('SQL Query:', sql_query)

if output.is_final_output:  # A condition to prevent executing invalid queries
    """
    Before using this execute_command function, certain environmental variables must be set
    DB_NAME = <name_of_database>
    USERNAME = <user_name>
    PASSWORD = <password>
    HOST = <host url of the database>
    PORT = <port number of the database>
    """
    print('SQL Output with Mock Database:', execute_command(sql_query))

if output.is_final_output:  # A condition to prevent executing invalid queries
    """
    If you want to execute to custom database server
    """
    params = {
        # Use Custom values instead of this environmental variables
        'dbname': os.environ.get("DB_NAME"),
        'user': os.environ.get("USERNAME"),
        'password': os.environ.get("PASSWORD"),
        'host': os.environ.get("HOST"),
        'port': os.environ.get("PORT")
    }
    print('SQL Output with Custom Database:',
          connect_and_execute_command(params, sql_query))


"""
Sample Terminal Output:

Enter your question here: What is the sum total of visitors that have accessed lead domain meta.com within the $100k-$1M revenue range?
SQL Query: SELECT SUM(no_of_visiting_ips) 
FROM website_aggregates 
WHERE lead_domain = 'meta.com' 
AND annual_revenue >= 100000 
AND annual_revenue <= 1000000;
SQL Output with Mock Database: [(Decimal('290889'),)]
SQL Output with Custom Database: [(Decimal('290889'),)]
"""