from text_to_sql import create_model, get_sql_query

"""
Creating the output using default model
Default Model : 'GPT 3.5 Turbo 16k'
"""
# !Important OPENAI_API_KEY should be added in the environment variable before calling this function
model = create_model()

query = input('Enter your question here: ')

model.load_schema_as_string("""
    CREATE TABLE website_aggregates (
        id SERIAL PRIMARY KEY,
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
    );


    GUIDELINES:
    - for count/total/number of visitors you must return sum of no_of_visiting_ips
    - for count/total/number of hits you must return sum of no_of_hits
    - if just domain is mentioned, always compare it with customer_domain
    - if 'lead' is mentioned before domain name, compare it lead_domain
    - if country name is abbreviated, use full name of the country
    - industry name should always be in lowercase
    - visitors and users can be used interchangeably 
    - For employee ranges always use estimated number of employees to compare
    - For revenue ranges always use annual revenue to compare, don't use revenue_range
    - For rolling window type questions, remember to use partition by 
""")

output = get_sql_query(model, query)

print('SQL Query: ', output.message)

"""
Sample Terminal Output:

Enter your question here: Give me all the users visiting meta.com in the year 2022  
SQL Query: SELECT * FROM website_aggregates WHERE customer_domain ILIKE '%meta.com' AND dt >= '2022-01-01' AND dt <= '2022-12-31'
"""
