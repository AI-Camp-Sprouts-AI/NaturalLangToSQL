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

from src.text_to_sql import create_model
from src.text_to_sql.database_connector import execute_command
from decimal import Decimal
from pathlib import Path
from pytest_check import check
import datetime

CWD = Path(__file__).parent

testcases = [
    {
        "input": "How many books does each author in the library have?",
        "output": "",
        "sql_output": "SELECT author, COUNT(book_id) AS book_count FROM library_books GROUP BY author;",
        "description": "This query uses GROUP BY to count the number of books each author has in the library."
    },
    {
        "input": "What is the total count of books borrowed by each member?",
        "output": "",
        "sql_output": "SELECT member_id, COUNT(book_id) AS borrowed_books FROM books_lent GROUP BY member_id;",
        "description": "This query uses GROUP BY to count the books borrowed by each library member."
    },
    {
        "input": "Display the top 5 details of books lent along with the member's name who borrowed them, including books that haven't been returned yet.",
        "output": [('6b7845a9ffe84b5414591b04b0931fb873b9077dc0befb1cfcd15b52da2398c7', 'Little Fires Everywhere', '4a4b210ef84a96c507deb052995d56c1e424bb044b10e4950c0af772c9d13920', 'Aria Nelson', datetime.date(2023, 11, 8)), ('826dc963f8f8e7217639f31e47ffc5f7fdaaa0d548802c4d2a8d3bcc2a172dc1', 'The Jasmine Throne', 'f56e36b0fc5a092a74e4bd4883e64e841f05eb0301d741bb97b14be8d9fb2b62', 'Bella Brooks', datetime.date(2023, 11, 10)), ('d07e31cf6e09192ef297d04584f8732bf94224f44c34bf07643576d7a02be689', "The Handmaid's Tale", 'ae6ac24b62fa4aa9d88cfd0440f66932a9fd5f320bcc4e1df90c4583779cede4', 'Nora Richardson', datetime.date(2023, 10, 26)), ('39cd6a0a874588d070833e58e3a802be36f7aa000a52c05108f06b353b93305f', 'The Giver of Stars', '05476be2400f3cf6ad1d4f248db260ed376c5611b462b0e913dfaee8e2cf4a15', 'Ellie James', datetime.date(2023, 11, 11)), ('af8ee3fa9803eb904d5186f892cde67098f1fb617e9dbb19d57eb82168aae236', 'The Chosen and the Beautiful', '39a59c29d97ee580eb30e1f78cea6dfd75e2527d93efe9843c0a54594d22f13c', 'Layla Cooper', datetime.date(2023, 10, 27))],
        "sql_output": "SELECT bl.book_id, lb.title, bl.member_id, lm.name, bl.lend_date FROM books_lent bl LEFT JOIN library_books lb ON bl.book_id = lb.book_id LEFT JOIN library_members lm ON bl.member_id = lm.member_id limit 5;",
        "description": "This query uses LEFT JOIN to display details of books lent and the corresponding members' names, including books that haven't been returned."
    },
    {
        "input": "List the books lent with their titles and the corresponding members' names who borrowed them.",
        "output": "",
        "sql_output": "SELECT bl.book_id, lb.title, bl.member_id, lm.name FROM books_lent bl INNER JOIN library_books lb ON bl.book_id = lb.book_id INNER JOIN library_members lm ON bl.member_id = lm.member_id;",
        "description": "This query uses INNER JOIN to display books lent with titles and the corresponding borrowing members' names."
    },
    {
        "input": "Show all books in the library along with the member's name who borrowed them (if borrowed), even if the book isn't lent out.",
        "output": "",
        "sql_output": "SELECT lb.book_id, lb.title, bl.member_id, lm.name FROM library_books lb LEFT JOIN books_lent bl ON lb.book_id = bl.book_id LEFT JOIN library_members lm ON bl.member_id = lm.member_id;",
        "description": "This query uses LEFT JOIN to show all books with the member's name who borrowed them (if borrowed), including books not lent out."
    },
    {
        "input": "Display the list of books borrowed along with their titles and the member's name who borrowed them, including books that haven't been returned yet.",
        "output": "",
        "sql_output": "SELECT bl.book_id, lb.title, bl.member_id, lm.name, bl.lend_date, bl.return_date FROM books_lent bl RIGHT JOIN library_books lb ON bl.book_id = lb.book_id LEFT JOIN library_members lm ON bl.member_id = lm.member_id;",
        "description": "This query uses RIGHT JOIN to display the list of borrowed books with titles and the borrowing members' names, including books not yet returned."
    },
    {
        "input": "What is the total count of books lent out from the library?",
        "output": "",
        "sql_output": "SELECT SUM(count) AS total_books_lent FROM library_books;",
        "description": "This query calculates the total count of books that have been lent out from the library."
    },
    {
        "input": "Which member has borrowed the most number of books?",
        "output": "",
        "sql_output": "SELECT member_id, COUNT(book_id) AS borrowed_count FROM books_lent GROUP BY member_id ORDER BY borrowed_count DESC LIMIT 1;",
        "description": "This query identifies the member who has borrowed the most number of books."
    },
    {
        "input": "How many books has a specific member borrowed so far?",
        "output": "",
        "sql_output": "SELECT member_id, COUNT(book_id) AS borrowed_count FROM books_lent WHERE member_id = '<specific_member_id>' GROUP BY member_id;",
        "description": "This query counts the number of books a specific member has borrowed so far."
    },
    {
        "input": "What are the titles of books lent out to a particular library member?",
        "output": "",
        "sql_output": "SELECT lb.title FROM library_books lb INNER JOIN books_lent bl ON lb.book_id = bl.book_id WHERE bl.member_id = '<specific_member_id>';",
        "description": "This query retrieves the titles of books lent out to a particular library member."
    },
    {
        "input": "How many books are currently available in the library for borrowing?",
        "output": "",
        "sql_output": "SELECT SUM(count) AS total_available_books FROM library_books;",
        "description": "This query calculates the total count of books currently available for borrowing in the library."
    },
    {
        "input": "Who are the top three authors with the most books in the library's collection?",
        "output": "",
        "sql_output": "SELECT author, COUNT(book_id) AS book_count FROM library_books GROUP BY author ORDER BY book_count DESC LIMIT 3;",
        "description": "This query identifies the top three authors with the most books in the library's collection."
    },
    {
        "input": "What is the average number of books borrowed per member?",
        "output": "",
        "sql_output": "SELECT AVG(borrowed_count) AS avg_books_borrowed FROM (SELECT member_id, COUNT(book_id) AS borrowed_count FROM books_lent GROUP BY member_id) AS counts;",
        "description": "This query calculates the average number of books borrowed per member."
    },
    {
        "input": "Which books have been borrowed the most times?",
        "output": "",
        "sql_output": "SELECT lb.title, COUNT(bl.book_id) AS borrowed_count FROM library_books lb INNER JOIN books_lent bl ON lb.book_id = bl.book_id GROUP BY lb.title ORDER BY borrowed_count DESC;",
        "description": "This query identifies the books that have been borrowed the most times."
    },
    {
        "input": "Can you list the books that haven't been lent out yet?",
        "output": "",
        "sql_output": "SELECT lb.title FROM library_books lb LEFT JOIN books_lent bl ON lb.book_id = bl.book_id WHERE bl.book_id IS NULL;",
        "description": "This query lists the books that haven't been lent out yet."
    },
    {
        "input": "How many books were lent out in the past month?",
        "output": "",
        "sql_output": "SELECT COUNT(book_id) AS books_lent_past_month FROM books_lent WHERE lend_date >= CURRENT_DATE - INTERVAL '1 month';",
        "description": "This query counts the number of books lent out in the past month."
    }
]

# print(
#     execute_command(
#         """
#     SELECT bl.book_id, lb.title, bl.member_id, lm.name, bl.lend_date FROM books_lent bl LEFT JOIN library_books lb ON bl.book_id = lb.book_id LEFT JOIN library_members lm ON bl.member_id = lm.member_id limit 5;
#         """
#     )
# )


def check_value(value, expected, info=''):
    with check:
        assert expected == value, info

def accuracy():
    NO_OF_REPETITIONS = 1
    model = create_model()
    schema_path = '../../data/schemas/library_test.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

    for testcase in testcases[:1]:
        for i in range(NO_OF_REPETITIONS):
            user_input = testcase['input']
            expected_output = testcase['output']
            if expected_output:
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
