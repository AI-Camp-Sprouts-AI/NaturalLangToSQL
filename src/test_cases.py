_websites_schema = """
CREATE TABLE website_aggregates (
    dt DATE, -- The date of the data entry.
    customer_domain VARCHAR(255), -- The domain name of the customer.
    lead_domain VARCHAR(255), -- The domain name of the lead.
    ip_country VARCHAR(255), -- The country associated with the IP address. Nullable.
    no_of_visiting_ips BIGINT, -- The number of unique IP addresses that visited.
    no_of_hits BIGINT, -- The total number of hits or visits.
    lead_domain_name VARCHAR(255), -- The name of the lead's domain.
    industry VARCHAR(255), -- The industry category the lead belongs to. Choices include 'financial services', 'healthcare', etc.
    estimated_num_employees INT, -- An estimate of the number of employees in the lead's company.
    city VARCHAR(255), -- The city where the lead is based.
    state VARCHAR(255), -- The state where the lead is based.
    company_country VARCHAR(255), -- The country where the lead's company is located.
    annual_revenue FLOAT, -- The annual revenue of the lead's company.
    total_funding FLOAT, -- The total funding received by the lead's company.
    latest_funding_stage VARCHAR(255), -- The most recent funding stage of the lead's company, like 'Series A', 'Seed', etc.
    status VARCHAR(255), -- The status of the lead. Options are 'Qualified', 'Disqualified', 'NA', 'NULL'.
    decayed_inbound_score DOUBLE, -- A decayed score based on inbound metrics. Nullable.
    decayed_intent_score DOUBLE, -- A decayed score based on intent metrics. Nullable.
    decayed_clubbed_score DOUBLE, -- A combined decayed score from various metrics. Nullable.
    last_visit_date DATE, -- The date of the last visit by the lead.
    employee_range VARCHAR(255), -- A range indicating the number of employees in the lead's company.
    revenue_range VARCHAR(255) -- A range indicating the annual revenue of the lead's company.
);
"""

"""
    {
        'prompt': "How many total visitors have visited the customer domain cruz.com?",
        'schema': _websites_schema,
        'correct_query': "SELECT SUM(no_of_visiting_ips) FROM website_aggregates WHERE customer_domain = 'cruz.com';",
        'valid_prompt': True
    },
"""

test_cases = [
    # BASIC RETRIEVAL
    {
        'summary': "Testing simple SELECT query to retrieve all data",
        'prompt': "Can you show me everything from the website aggregates?",
        'schema': _websites_schema,
        'correct_query': "SELECT * FROM website_aggregates;",
        'valid_prompt': True
    },
    {
        'summary': "Testing retrieval of specific columns (customer_domain and ip_country)",
        'prompt': "What are the domains and countries of customers?",
        'schema': _websites_schema,
        'correct_query': "SELECT customer_domain, ip_country FROM website_aggregates;",
        'valid_prompt': True
    },

    # CONDITIONAL QUERIES
    {
        'summary': "Testing WHERE clause with a specific date filter",
        'prompt': "Can you tell me the total number of hits we had on the first day of 2023?",
        'schema': _websites_schema,
        'correct_query': "SELECT SUM(no_of_hits) FROM website_aggregates WHERE dt = '2023-01-01';",
        'valid_prompt': True
    },
    {
        'summary': "Testing WHERE clause with AND operator combining industry and country filters",
        'prompt': "I need the list of lead domains in the healthcare industry from the United States.",
        'schema': _websites_schema,
        'correct_query': "SELECT lead_domain FROM website_aggregates WHERE industry = 'healthcare' AND company_country = 'United States';",
        'valid_prompt': True
    },
    {
        'summary': "Testing WHERE clause combining OR and NOT operators",
        'prompt': "Show me the details of leads who are either in the financial services or healthcare industry but are not from New York.",
        'schema': _websites_schema,
        'correct_query': "SELECT * FROM website_aggregates WHERE (industry = 'financial services' OR industry = 'healthcare') AND NOT state = 'New York';",
        'valid_prompt': True
    },

    # AGGREGATION & GROUPING
    {
        'summary': "Testing aggregate function SUM to calculate total hits",
        'prompt': "What's the total number of hits we've had?",
        'schema': _websites_schema,
        'correct_query': "SELECT SUM(no_of_hits) FROM website_aggregates;",
        'valid_prompt': True
    },
    {
        'summary': "Testing AVG function grouped by industry",
        'prompt': "Can you tell me the average number of employees in each industry?",
        'schema': _websites_schema,
        'correct_query': "SELECT industry, AVG(estimated_num_employees) FROM website_aggregates GROUP BY industry;",
        'valid_prompt': True
    },
    {
        'summary': "Testing GROUP BY with HAVING clause for filtering on aggregated data",
        'prompt': "Show me industries where the average annual revenue is more than 500000.",
        'schema': _websites_schema,
        'correct_query': "SELECT industry FROM website_aggregates GROUP BY industry HAVING AVG(annual_revenue) > 500000;",
        'valid_prompt': True
    },

    # JOIN OPERATIONS
    
    # These don't work with only one table
    #{
    #    'summary': "Testing INNER JOIN between website_aggregates and a hypothetical customer_details table",
    #    'prompt': "Can you show me the customer domains and their names from both tables?",
    #    'schema': _websites_schema,
    #    'correct_query': "SELECT website_aggregates.customer_domain, customer_details.customer_name FROM website_aggregates INNER JOIN customer_details ON website_aggregates.customer_domain = customer_details.domain;",
    #    'valid_prompt': True
    #},
    #{
    #    'summary': "Testing LEFT OUTER JOIN to find unmatched records in the primary table",
    #    'prompt': "I want to see all lead domains and any corresponding customer names, even if there's no match.",
    #    'schema': _websites_schema,
    #    'correct_query': "SELECT website_aggregates.lead_domain, customer_details.customer_name FROM website_aggregates LEFT JOIN customer_details ON website_aggregates.lead_domain = customer_details.domain;",
    #    'valid_prompt': True
    #},
    #
    #{
    #    'summary': "Testing Self Join to compare records within the same table",
    #    'prompt': "Show me leads that have visited on the same day but are from different countries.",
    #    'schema': _websites_schema,
    #    'correct_query': "SELECT a.lead_domain, b.lead_domain FROM website_aggregates a JOIN website_aggregates b ON a.dt = b.dt WHERE a.ip_country != b.ip_country;",
    #    'valid_prompt': True
    #},

    # SUBQUERIES
    {
        'summary': "Testing subquery within WHERE clause to filter data",
        'prompt': "Can you show me the details of leads who visited more than the average number of visits?",
        'schema': _websites_schema,
        'correct_query': "SELECT * FROM website_aggregates WHERE no_of_visiting_ips > (SELECT AVG(no_of_visiting_ips) FROM website_aggregates);",
        'valid_prompt': True
    },
    {
        'summary': "Testing subquery used as a table in FROM clause",
        'prompt': "I want to see the average number of hits per country.",
        'schema': _websites_schema,
        'correct_query': "SELECT avg_hits_per_country.ip_country, AVG(avg_hits_per_country.no_of_hits) FROM (SELECT ip_country, no_of_hits FROM website_aggregates) AS avg_hits_per_country GROUP BY avg_hits_per_country.ip_country;",
        'valid_prompt': True
    },
    {
        'summary': "Testing nested subquery for complex data retrieval",
        'prompt': "Show me leads from countries that have more than 10 unique visiting IPs on average.",
        'schema': _websites_schema,
        'correct_query': "SELECT lead_domain, ip_country FROM website_aggregates WHERE ip_country IN (SELECT ip_country FROM website_aggregates GROUP BY ip_country HAVING AVG(no_of_visiting_ips) > 10);",
        'valid_prompt': True
    },

    # SET OPERATIONS
    {
        'summary': "Testing UNION to combine results from multiple queries",
        'prompt': "Can you show me a list of both customer and lead domains?",
        'schema': _websites_schema,
        'correct_query': "SELECT customer_domain AS domain FROM website_aggregates UNION SELECT lead_domain FROM website_aggregates;",
        'valid_prompt': True
    },
    {
        'summary': "Testing INTERSECT to find common elements between two queries",
        'prompt': "I want to know which domains are both customer and lead domains.",
        'schema': _websites_schema,
        'correct_query': "SELECT customer_domain FROM website_aggregates INTERSECT SELECT lead_domain FROM website_aggregates;",
        'valid_prompt': True
    },
    {
        'summary': "Testing EXCEPT to find elements in one query not present in another",
        'prompt': "Show me the domains that are customer domains but not lead domains.",
        'schema': _websites_schema,
        'correct_query': "SELECT customer_domain FROM website_aggregates EXCEPT SELECT lead_domain FROM website_aggregates;",
        'valid_prompt': True
    },

    # ORDERING & LIMITING
    {
        'summary': "Testing ORDER BY clause for sorting based on a specific column",
        'prompt': "Can you list all leads in order of their last visit date?",
        'schema': _websites_schema,
        'correct_query': "SELECT * FROM website_aggregates ORDER BY last_visit_date DESC;",
        'valid_prompt': True
    },
    {
        'summary': "Testing LIMIT clause to restrict the number of results",
        'prompt': "Show me the top 5 leads based on the number of visiting IPs.",
        'schema': _websites_schema,
        'correct_query': "SELECT * FROM website_aggregates ORDER BY no_of_visiting_ips DESC LIMIT 5;",
        'valid_prompt': True
    },
    {
        'summary': "Combining ORDER BY and LIMIT clauses for sorted and limited results",
        'prompt': "I need the names of the top 3 industries with the highest average annual revenue.",
        'schema': _websites_schema,
        'correct_query': "SELECT industry, AVG(annual_revenue) AS avg_revenue FROM website_aggregates GROUP BY industry ORDER BY avg_revenue DESC LIMIT 3;",
        'valid_prompt': True
    },
    # COMPLEX QUERIES
    {
        'summary': "Testing a combination of JOIN and subquery",
        'prompt': "Can you show me the customer domains and the average number of hits for each, but only for those customers who had visits on or after January 1, 2023?",
        'schema': _websites_schema,
        'correct_query': "SELECT a.customer_domain, AVG(a.no_of_hits) FROM website_aggregates a JOIN (SELECT DISTINCT customer_domain FROM website_aggregates WHERE dt >= '2023-01-01') b ON a.customer_domain = b.customer_domain GROUP BY a.customer_domain;",
        'valid_prompt': True
    },
    {
        'summary': "Testing GROUP BY and HAVING in combination with aggregate functions",
        'prompt': "I need to know which industries had more than 3 different leads last month.",
        'schema': _websites_schema,
        'correct_query': "SELECT industry FROM website_aggregates WHERE dt >= CURRENT_DATE - INTERVAL '1 month' GROUP BY industry HAVING COUNT(DISTINCT lead_domain) > 3;",
        'valid_prompt': True
    },
    {
        'summary': "Testing complex query with CASE statement",
        'prompt': "Show me the lead domains and classify their visit frequency as 'High', 'Medium', or 'Low' based on the number of visiting IPs being greater than 100, between 50 and 100, and less than 50, respectively.",
        'schema': _websites_schema,
        'correct_query': "SELECT lead_domain, CASE WHEN no_of_visiting_ips > 100 THEN 'High' WHEN no_of_visiting_ips BETWEEN 50 AND 100 THEN 'Medium' ELSE 'Low' END AS visit_frequency FROM website_aggregates;",
        'valid_prompt': True
    },

    # DATA TYPES
    {
        'summary': "Testing date function for calculating age of data entries",
        'prompt': "How old are the entries in our website aggregates table?",
        'schema': _websites_schema,
        'correct_query': "SELECT dt, CURRENT_DATE - dt AS age_of_entry FROM website_aggregates;",
        'valid_prompt': True
    },
    {
        'summary': "Testing string function for concatenating columns",
        'prompt': "Can you give me the full names of leads combining city and state?",
        'schema': _websites_schema,
        'correct_query': "SELECT city || ', ' || state AS full_location FROM website_aggregates;",
        'valid_prompt': True
    },
    {
        'summary': "Testing string manipulation function to extract substrings",
        'prompt': "I need the first three letters of each lead's country.",
        'schema': _websites_schema,
        'correct_query': "SELECT SUBSTRING(company_country FROM 1 FOR 3) FROM website_aggregates;",
        'valid_prompt': True
    },

    # MODIFICATON
    {
        'summary': "Attempting to insert data into the table",
        'prompt': "Add a new record to the website aggregates with today's date and some data.",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Attempting to update existing data in the table",
        'prompt': "Change the number of hits to 500 for all entries from yesterday.",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Attempting to delete data from the table",
        'prompt': "Remove all records from the website aggregates where the status is 'Disqualified'.",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },

    # AMBIGUOUS QUERIES
    {
        'summary': "Query is ambiguous due to lack of specific details about what data to retrieve",
        'prompt': "Can you show me the records?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Query lacks a specific time frame for data retrieval",
        'prompt': "I want to see the number of hits, but when exactly?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Query is partially complete but missing information about which industry",
        'prompt': "How many leads do we have in which industry?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },

    # UNRELATED QUERIES
    {
        'summary': "Query is unrelated to the database and pertains to general knowledge",
        'prompt': "What is the capital of France?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Query asking for information not contained within the database",
        'prompt': "Can you tell me the latest stock prices?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Query seeking personal advice, irrelevant to database querying",
        'prompt': "What should I have for dinner tonight?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },

    # REFINEMENT
    {
        'summary': "Query is too broad and lacks specificity about the data required",
        'prompt': "Tell me something about our website data.",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Query lacks specific metrics or dimensions to focus on",
        'prompt': "Can you give me some statistics from the data?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    },
    {
        'summary': "Query is general and does not define a clear objective or data point",
        'prompt': "What can you show me about our customers?",
        'schema': _websites_schema,
        'correct_query': "",
        'valid_prompt': False
    }
]