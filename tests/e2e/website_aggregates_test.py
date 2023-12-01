import threading
import random
import time

from tqdm import tqdm
from decimal import Decimal
from src.text_to_sql import create_model
from src.text_to_sql.database_connector import create_new_connection_and_execute
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
}, {
    "questions": [
        "What is the total number of hits from the companies in California?",
        "How many hits, in total, were made by companies located in California?",
        "Could you tell me the overall number of hits from California-based companies?",
        "What's the total count of hits originating from companies in California?",
        "Count the total number of hits from companies situated in California.",
        "I'm interested in knowing the total number of hits made by California-based companies. Can you provide that?",
        "How many hits have been registered from companies in California?",
        "Provide the total count of hits from companies in California, please.",
        "Tell me the overall number of hits from the companies based in California.",
        "What is the total count of hits originating from companies in California?",
        "Could you give me the total number of hits from companies located in California?",
        "How many hits were generated by companies in California?",
        "I'd like to know the total number of hits from companies in California.",
        "Can you provide the total count of hits from companies in California?",
        "Give me the total number of hits from companies in California.",
        "What's the total count of hits from California-based companies?",
        "I'm curious about the total number of hits from companies in California.",
        "What is the overall count of hits from companies situated in California?",
        "Could you share the total number of hits from companies in California?",
        "Tell me the count of hits from companies in California.",
        "Provide the total number of hits from companies in California."
    ],
    "output": [(Decimal('2954'),)],
    "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE state = 'California';"
}, {
    "questions": [
        "Provide the count of visitors from the United States grouped by lead domain.",
        "What is the visitor count from the United States grouped by lead domain?",
        "Could you give me the number of visitors from the US categorized by lead domain?",
        "I'm interested in knowing the count of visitors from the United States grouped by their lead domain. Can you provide that?",
        "Provide me with the visitor count from the US grouped by lead domain, please.",
        "What is the total number of visitors from the United States organized by lead domain?",
        "Can you give me the count of visitors from the US grouped by their lead domain?",
        "I'd like to know the visitor count from the United States categorized by lead domain.",
        "Could you provide the count of visitors from the United States, categorized by their lead domain?",
        "Tell me the count of visitors from the US grouped by lead domain.",
        "What is the total visitor count from the United States categorized by their lead domain?",
        "Provide the count of visitors from the United States, grouped by lead domain.",
        "How many visitors from the US are categorized by lead domain?",
        "I'm curious about the visitor count from the United States grouped by lead domain.",
        "Can you provide me with the count of visitors from the US categorized by their lead domain?",
        "Give me the visitor count from the United States grouped by lead domain.",
        "What's the count of visitors from the US grouped by lead domain?",
        "I'd like to know how many visitors from the United States are grouped by their lead domain.",
        "Provide me with the count of visitors from the US grouped by their lead domain, please.",
        "Can you give me the number of visitors from the United States grouped by lead domain?",
        "Tell me the visitor count from the US grouped by lead domain."
    ],
    "output": [('brave.com', Decimal('6593')), ('samsung.com', Decimal('3330')), ('tesla.com', Decimal('3619'))],
    "sql_output": "SELECT lead_domain, SUM(no_of_visiting_ips) FROM website_aggregates WHERE ip_country = 'United States' GROUP BY lead_domain;"
}, {
    "questions": [
        "Display the count of hits for telecommunications industry companies situated in Douglasfort.",
        "What is the number of hits for companies in the telecommunications sector based in Douglasfort?",
        "Could you show the hits count for companies in the telecommunications industry located in Douglasfort?",
        "Show me the hits count for telecommunications sector companies in Douglasfort.",
        "What's the count of hits for companies in the telecommunications industry in Douglasfort?",
        "Display the number of hits for telecommunications-related companies in Douglasfort.",
        "I'd like to know the hits count for telecommunications industry companies located in Douglasfort.",
        "What is the number of hits for companies in the telecommunications sector in Douglasfort?",
        "Could you display the hits count for telecommunications companies in Douglasfort?",
        "Show the hits count for companies in the telecommunications industry located in Douglasfort.",
        "What's the hits count for companies in the telecommunications industry in Douglasfort?",
        "Display the number of hits for telecommunications companies situated in Douglasfort.",
        "I'm interested in the hits count for companies in the telecommunications industry located in Douglasfort. Can you provide that?",
        "What is the hits count for telecommunications-related companies in Douglasfort?",
        "Could you show the hits count for telecommunications sector companies in Douglasfort?",
        "Show me the hits count for companies in the telecommunications industry in Douglasfort.",
        "What's the count of hits for companies in the telecommunications field in Douglasfort?",
        "Display the number of hits for telecommunications industry companies located in Douglasfort.",
        "I'd like to know the hits count for telecommunications companies in Douglasfort.",
        "What is the hits count for companies in the telecommunications industry located in Douglasfort?"
    ],
    "output": [(Decimal('29'),)],
    "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE industry = 'telecommunications' and city = 'Douglasfort';"
}, {
    "questions": [
        "Count the total number of customers whose annual revenue is over 100k.",
        "Could you tell me the total count of customers with an annual revenue above 100k?",
        "I'm interested in knowing the total number of customers with annual revenue exceeding 100k. Can you provide that?",
        "What's the overall count of customers with an annual revenue above hundred thousand?",
        "How many customers, in total, have an annual revenue higher than 100k?",
        "Provide the total count of customers with an annual revenue exceeding 100k, please.",
        "Tell me the total number of customers whose annual revenue is above 100k.",
        "What is the total count of customers with annual revenue greater than 100,000?",
        "Could you give me the total number of customers with an annual revenue above 100,000?",
        "How many customers have annual revenue above 100,000 in total?",
        "I'd like to know the count of customers with an annual revenue above 100,000.",
        "Provide the total count of customers whose annual revenue exceeds 100k.",
        "Count the total number of customers with annual revenue surpassing 100k.",
        "What is the count of customers with an annual revenue that exceeds 100000?",
        "I'm curious about the total number of customers with annual revenue above 100000.",
        "How many customers have an annual revenue greater than 100k in total?",
        "Could you share the total count of customers with an annual revenue above 100k?",
        "Tell me the total number of customers having annual revenue over 100k.",
        "What is the total number of customers with an annual revenue over 100k?"
    ],
    "output": [(3292,)],
    "sql_output": "SELECT COUNT(*) FROM website_aggregates WHERE annual_revenue > 100000;"
}, {
    "questions": [
        "Could you display top 5 lead domains with more than 500 visiting IPs?",
        "Can you show the top 5 lead domains that have over 500 visiting IPs?",
        "Please present the top 5 lead domains with more than 500 visiting IPs.",
        "I'd like to see the top 5 lead domains that have at least 500 visiting IPs. Could you display those?",
        "Display the top 5 lead domains having more than 500 visiting IPs, please.",
        "Could you list the top 5 lead domains with over 500 visiting IPs?",
        "Show me the top 5 lead domains that have a count of visiting IPs exceeding 500.",
        "I'm interested in seeing the top 5 lead domains with more than 500 visiting IPs. Can you display them?",
        "Please provide the top 5 lead domains having over 500 visiting IPs.",
        "Can you list the top 5 lead domains that have a visiting IP count of 500 or more?",
        "I'd like to view the top 5 lead domains with more than 500 visiting IPs, could you show those?",
        "Show the top 5 lead domains with over 500 visiting IPs, please.",
        "Could you display the top 5 lead domains that have more than 500 visiting IPs?",
        "I want to see the top 5 lead domains that have more than 500 visiting IPs. Can you display them?",
        "Display top 5 lead domains with visiting IPs greater than 500, please.",
        "Can you show me the top 5 lead domains with over 500 visiting IPs?",
        "I'm looking for the top 5 lead domains that have more than 500 visiting IPs. Could you display them?",
        "List the top 5 lead domains with more than 500 visiting IPs, please.",
        "Could you display the top 5 lead domains having more than 500 visiting IPs?",
        "Show the top 5 lead domains that have more than 500 visiting IPs, please.",
        "Please present the top 5 lead domains having more than 500 visiting IPs."
    ],
    "output": [('meta.com', Decimal('314948')), ('tesla.com', Decimal('307297')), ('facebook.com', Decimal('305623')), ('apple.com', Decimal('290653')), ('microsoft.com', Decimal('288525'))],
    # Having, Where - Conflict
    "sql_output": """
        SELECT lead_domain, SUM(no_of_visiting_ips) 
        FROM website_aggregates 
        GROUP BY lead_domain 
        HAVING SUM(no_of_visiting_ips) > 500 
        ORDER BY SUM(no_of_visiting_ips) DESC 
        LIMIT 5;
    """
}, {
    "questions": [
        "Show the total number of hits for companies with a funding stage of 'Series A'.",
        "Display the overall count of hits for companies at the 'Series A' funding stage.",
        "What is the total number of hits recorded for companies in the 'Series A' funding stage?",
        "Show the sum total of hits for companies that are in the 'Series A' funding round.",
        "Could you provide the total count of hits specifically for companies with a funding stage of 'Series A'?",
        "I'm interested in knowing the total hits for companies categorized under the 'Series A' funding stage. Can you display that?",
        "What's the aggregate count of hits for companies at the 'Series A' funding stage?",
        "Show the total hits for companies that are currently in the 'Series A' funding round.",
        "I'd like to see the total number of hits for companies with a funding stage of 'Series A'.",
        "Could you display the sum total of hits for companies at the 'Series A' funding stage?",
        "Provide the total count of hits for companies classified in the 'Series A' funding stage.",
        "What is the total number of hits for companies at the 'Series A' funding stage?",
        "Show the count of hits for companies that have a funding stage of 'Series A'.",
        "I'm curious about the total hits for companies that are at the 'Series A' funding stage.",
        "Display the total count of hits for companies that belong to the 'Series A' funding round.",
        "What's the total number of hits for companies categorized under the 'Series A' funding stage?",
        "Could you show the total count of hits for companies currently in the 'Series A' funding round?",
        "I'd like to know the total hits for companies in the 'Series A' funding stage.",
        "What is the total count of hits for companies having a funding stage of 'Series A'?",
        "Show the total hits for companies that have reached the 'Series A' funding stage.",
        "Provide the total count of hits for companies involved in the 'Series A' funding stage."
    ],
    "output": [(Decimal('10050'),)],
    "sql_output": "SELECT SUM(no_of_hits) FROM website_aggregates WHERE latest_funding_stage = 'Series A';"
}, {
    "questions": [
        "Provide the count of visitors from companies in the retail industry with decayed intent score above 0.8.",
        "What is the count of visitors from retail business companies with an intent score above 0.8?",
        "How many visitors are there from companies in the retail business with an intent score exceeding 0.8?",
        "Count the number of visitors from retail business companies with an intent score above 0.8.",
        "Could you tell me the number of visitors from companies in the retail business with an intent score higher than 0.8?",
        "I'm interested in knowing the count of visitors from retail sector companies with an intent score above 0.8. Can you provide that?",
        "What's the total count of visitors from companies in the retail sector with an intent score above 0.8?",
        "How many visitors from retail sector companies have an intent score above 0.8?",
        "Provide the count of visitors with decayed intent score above 0.8 from companies in the retail industry, please.",
        "Tell me the total count of visitors from retail industry companies with an intent score greater than 0.8.",
        "What is the count of visitors with decayed intent score above 0.8 from companies in the retail industry?",
        "I'd like to know the total number of visitors from enterprises in the retail industry with an intent score above 0.8.",
        "Could you give me the count of visitors from retail field enterprises with an intent score above 0.8?",
        "Provide the number of visitors with decayed intent score above 0.8 from companies in the retail field.",
        "How many visitors from companies in the retail field have an intent score above 0.8 in total?",
        "What's the total number of visitors from companies in the retail field with an intent score above 0.8?",
        "I'm curious about the count of visitors from companies in the retail industry with an intent score above 0.8.",
        "What is the number of visitors from companies in the retail industry with an intent score above 0.8?",
        "Could you share the count of visitors from companies in the retail industry with an intent score above 0.8?",
        "Tell me the count of visitors from companies in the retail industry with an intent score above 0.8.",
        "What is the total count of visitors from companies in the retail industry with an intent score above 0.8?"
    ],
    "output": [(Decimal('1012310'),)],
    "sql_output": "SELECT SUM(no_of_visiting_ips) FROM website_aggregates WHERE industry = 'retail' AND decayed_intent_score > 0.8;"
}, {
    "questions": [
        "Could you display the lead domains with Club score decay falling short of 0.3?",
        "Can you show the lead domains with a decayed clubbed score lower than 0.3?",
        "Display the lead domains having a Club score decay falling short of 0.3, please.",
        "I'm interested in seeing the lead domains with a decayed clubbed score below 0.3. Can you display those?",
        "What are the lead domains with a decayed clubbed score that's less than 0.3?",
        "Show me the lead domains where the decayed clubbed score is under 0.3.",
        "Could you list the lead domains that have a decayed clubbed score lower than 0.3?",
        "Display the lead domains having a Club score decay falling short of 0.3.",
        "Can you provide a list of lead domains with a decayed clubbed score below 0.3?",
        "Please show the lead domains with a decayed clubbed score less than 0.3.",
        "I'd like to see the lead domains with a decayed clubbed score that's less than 0.3. Can you display them?",
        "What are the lead domains whose decayed clubbed score is lower than 0.3?",
        "Could you show me the lead domains that have a decayed clubbed score lower than 0.3?",
        "Can you display the lead domains with a decayed clubbed score below 0.3?",
        "Show the lead domains that have a decayed clubbed score lower than 0.3, please.",
        "I want to view the lead domains with a decayed clubbed score below 0.3.",
        "What are the lead domains having a decayed clubbed score less than 0.3?",
        "Please display the lead domains with a decayed clubbed score less than 0.3.",
        "Can you list the lead domains with a decayed clubbed score below 0.3?",
        "Display the lead domains with a decayed clubbed score less than 0.3, please.",
        "Show the lead domains where the decayed clubbed score is less than 0.3."
    ],
    "output": [('carr.biz',)],
    "sql_output": "SELECT lead_domain, SUM(no_of_visiting_ips) FROM website_aggregates GROUP BY lead_domain HAVING SUM(decayed_clubbed_score) < 0.3;"
}, {
    "questions": [
        "Calculate the total number of hits over a rolling window of 30 days for each customer domain and list the top 5 results",
        "What are the total hits within a 30-day rolling window for each customer domain, listing the top 5 results?",
        "Can you compute the total number of hits within a 30-day rolling window for each customer domain and display the top 5 results?",
        "Calculate the total hits for each customer domain over a 30-day rolling window and show the top 5 results.",
        "I need the total number of hits over a rolling 30-day window for each customer domain, displaying the initial 5 results.",
        "What's the count of hits over a 30-day rolling window for each customer domain? Show the top 5 results.",
        "Compute the total hits within a rolling window of 30 days for each customer domain and display the initial 5 results.",
        "Could you calculate the total hits within a 30-day rolling window for each customer domain and show the top 5 results?",
        "List the top 5 results for the total number of hits over a rolling 30-day window for each customer domain.",
        "Provide the top 5 results for the total hits over a 30-day rolling window for each customer domain.",
        "What is the total count of hits over a rolling 30-day window for each customer domain? Show the top 5 results.",
        "Compute the total hits for each customer domain within a 30-day rolling window and display the top 5 results.",
        "Can you show me the initial 5 results for the total hits over a rolling window of 30 days for each customer domain?",
        "Calculate the total hits within a rolling 30-day window for each customer domain and list the initial 5 results.",
        "I'd like to see the top 5 results for the total number of hits over a rolling 30-day window for each customer domain.",
        "Display the top 5 results for the total hits over a rolling window of 30 days for each customer domain.",
        "Could you show the top 5 results for the total hits over a 30-day rolling window for each customer domain?",
        "Provide the initial 5 results for the total hits over a rolling window of 30 days for each customer domain.",
        "What are the top 5 results for the total hits over a 30-day rolling window for each customer domain?",
        "List the initial 5 results for the total number of hits over a rolling 30-day window for each customer domain.",
        "Show the top 5 results for the total hits over a rolling 30-day window for each customer domain."
    ],
    "output": [('bmw.com', Decimal('2538')), ('southwest.com', Decimal('2446')), ('boeing.com', Decimal('2439')), ('samsung.com', Decimal('2423')), ('google.com', Decimal('2248'))],
    "sql_output": """
        SELECT DISTINCT customer_domain,dt,
        SUM(no_of_hits) OVER (PARTITION BY customer_domain ORDER BY dt ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS total_hits_30_days
        FROM website_aggregates
        ORDER BY customer_domain, dt
        limit 5;
    """
}, {
    "questions": [
        "Display the top 5 results in ascending order of lead domain, showcasing the average decayed clubbed score over a rolling window of 1 week for each lead domain.",
        "Could you present the top 5 results in ascending order of lead domain, featuring the average decayed clubbed score over a rolling window of 1 week for each lead domain?",
        "Show me the first 5 results in ascending order of lead domain, illustrating the average decayed clubbed score over a rolling window of 1 week for each lead domain.",
        "I'm interested in seeing the first 5 results in ascending order of lead domain, with the average decayed clubbed score over a rolling window of 1 week for each lead domain. Can you show that?",
        "What are the first 5 results in ascending order of lead domain, presenting the mean of clubbed score decay over a rolling window of 1 week for each lead domain?",
        "Display the first 5 results sorted in ascending order of lead domain, showing the mean of clubbed score decay over a rolling window of 1 week for each lead domain.",
        "Can you list the first 5 results in ascending order of lead domain, including the mean of clubbed score decay over a rolling window of 7 days for each lead domain?",
        "I'd like to see the first 5 results in ascending order of lead domain, along with the mean of clubbed score decay over a rolling window of 7 days for each lead domain.",
        "Show the top 5 results ordered by lead domain in ascending order, with the mean of clubbed score decay over a rolling window of 7 days for each lead domain.",
        "What are the top 5 results ordered by lead domain in ascending order, displaying the average decayed clubbed score over a rolling window of 7 days for each lead domain?",
        "Display the top 5 rows in ascending order of lead domain, indicating the average decayed clubbed score over a rolling window of 7 days for each lead domain.",
        "I'm curious about the top 5 rows in ascending order of lead domain, featuring the average score of decay in clubbed score over a rolling window of 7 days for each lead domain.",
        "Can you provide the top 5 rows in ascending order of lead domain, including the average score of decay in clubbed score over a rolling window of 7 days for each lead domain?",
        "List the top 5 rows sorted in ascending order of lead domain, showcasing the average score of decay in clubbed score over a rolling window of 1 week for each lead domain.",
        "What are the top 5 results sorted in ascending order of lead domain, illustrating the average score of decay in clubbed score over a rolling window of 1 week for each lead domain?",
        "Could you show the top 5 results in ascending order of lead domain, along with the average decayed clubbed score over a rolling window of 1 week for each lead domain?",
        "Provide the first 5 entries in ascending order of lead domain, showing the average decayed clubbed score over a rolling window of 1 week for each lead domain.",
        "Show me the first 5 entries in ascending order of lead domain, featuring the average decayed clubbed score over a rolling window of 7 days for each lead domain.",
        "What are the first 5 entries in ascending order of lead domain, including the average decayed clubbed score over a rolling window of 7 days for each lead domain?",
        "List the top 5 results in ascending order of lead domain, indicating the average decayed clubbed score over a rolling window of 7 days for each lead domain."
    ],
    "output": [('abbott-miller.com', 747.0183), ('acevedo.info', 234.496), ('adams-bates.com', None), ('adams-bradley.com', 801.3413), ('adams-johnson.org', 463.0618)],
    "sql_output": """
        SELECT DISTINCT lead_domain,
        AVG(decayed_clubbed_score) OVER (PARTITION BY lead_domain ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_decayed_clubbed_score
        FROM website_aggregates
        ORDER BY lead_domain ASC
        limit 5
    """
}, {
    "questions":  [
        "Determine the maximum estimated employee count for each industry within a 14-day rolling window, presenting the top 5 results.",
        "What are the top 5 industries with the maximum estimated number of employees within a rolling 2 week window?",
        "Within a 2 week rolling period, identify the industries with the highest estimated employee count, listing the top 5 results.",
        "Can you find the count of maximum estimated number of employees for each industry within a 2 week rolling window, showing the top 5?",
        "List the top 5 industries with the count of maximum estimated employee within a rolling window of 14 days.",
        "Identify the top 5 industries by their maximum estimated employee count within a half month rolling window.",
        "What industries show the highest estimated employee counts within a half month rolling window, presenting the top 5 results?",
        "I'm interested in knowing the top 5 industries by their maximum estimated employee count within a half month rolling window. Can you provide that information?",
        "Could you display the industries with the highest estimated employee count within a half month rolling window, showing the top 5?",
        "Find the industries with the highest estimated employee counts within a rolling window of 14 days, listing the top 5 results.",
        "Provide the top 5 industries with the maximum estimated number of employees within a rolling 2 week window.",
        "What are the top 5 industries based on the maximum estimated number of employees within a rolling 2 week window?",
        "Which industries have the highest estimated employee counts within a 2 week rolling window, presenting the top 5 results?",
        "List the top 5 industries by their maximum estimated employee count within a rolling window of 14 days.",
        "Can you present the top 5 industries with the maximum estimated number of employees within a rolling 14-day window?",
        "What industries display the highest estimated employee counts within a 14-day rolling window, providing the top 5 results?",
        "Display the top 5 industries with the maximum estimated employee count within a 14-day rolling window.",
        "Please show the industries with the highest estimated employee counts within a rolling 14-day window, listing the top 5 results.",
        "What are the top 5 industries showing the maximum estimated number of employees within a rolling 14-day window?",
        "Identify the top 5 industries by their maximum estimated employee count within a rolling window of 14 days."
    ],
    "output": [('sports and recreation', 143159), ('healthcare', 106132), ('telecommunications', 102452), ('real estate', 101142), ('financial services', 98385)],
    "sql_output": """
        SELECT industry, SUM(estimated_num_employees) AS total_employees
        FROM website_aggregates
        WHERE dt >= CURRENT_DATE - INTERVAL '14 days'
        GROUP BY industry
        ORDER BY total_employees DESC
        LIMIT 5;
    """
}]

# Helper Functions


def linearize_testcases(testcases, no_of_repetitions=1):
    array = []
    for testcase in testcases:
        output = testcase['output']
        sql_output = testcase['sql_output']
        if len(output):
            questions = testcase['questions']
            for question in questions:
                array.append({
                    'input': question,
                    'output': output,
                    'sql_output': sql_output
                })
    array *= no_of_repetitions
    random.shuffle(array)
    return array


def split_into_batches(array, count=None):
    if count is None:
        count = len(array)
    batches = []
    i = 0
    while i < len(array):
        batches.append(array[i:i+count])
        i += count

    return batches


def check_value(value, expected, info=''):
    with check:
        assert expected == value, info


def run_model(testcase, schema_string=None):
    model = create_model()

    if schema_string is None:
        # schema_path = '../../data/schemas/website_aggregates.txt'
        # schema_path = CWD.joinpath(schema_path).absolute()
        # model.load_schema_from_file(schema_path)
        raise Exception('Schema string has to be specified')
    else:
        model.load_schema_as_string(schema_string)

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
NO_OF_REPETITIONS = 3
NO_OF_ASSERTIONS_PER_TEST = 2

testcases = list(filter(lambda x: len(x['output']), testcases))


testcases = linearize_testcases(testcases[:], NO_OF_REPETITIONS)


progress_bar = tqdm(total=len(testcases) * NO_OF_ASSERTIONS_PER_TEST,
                    desc='Assertions Completed')

# Entry Point for PyTest


def test_accuracy_of_model():
    batches = split_into_batches(testcases, count=50)
    batches_progress = tqdm(total=len(batches), desc='Batches Completed')
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    with open(schema_path, 'r') as f:
        schema_string = f.read()

    for set_of_testcases in batches:
        threads = []
        for testcase in set_of_testcases:
            threads.append(
                threading.Thread(
                    target=run_model,
                    args=[testcase, schema_string]
                )
            )
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        batches_progress.update(1)
        time.sleep(0.5)

    # # for set_of_testcases in batches:
    # threads = []
    # for testcase in testcases:
    #     threads.append(
    #         threading.Thread(
    #             target=run_model,
    #             args=[testcase, schema_string]
    #         )
    #     )
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    # # batches_progress.update(1)
    # time.sleep(0.5)


if __name__ == '__main__':
    # print(create_new_connection_and_execute("""
    #     SELECT industry, SUM(estimated_num_employees) AS total_employees
    #     FROM website_aggregates
    #     WHERE dt >= CURRENT_DATE - INTERVAL '14 days'
    #     GROUP BY industry
    #     ORDER BY total_employees DESC
    #     LIMIT 5;
    # """))
    test_accuracy_of_model()
    pass
