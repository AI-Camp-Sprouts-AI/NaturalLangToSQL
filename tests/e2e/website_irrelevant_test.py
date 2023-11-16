"""
Here the testcases for the function has to be added
This testcases should follow a format

[{
    input : '...' -> Input from user,
    description : '...' -> Any Description (Optional)
}]
"""

from src import create_model
from pathlib import Path

CWD = Path(__file__).parent

testcases = [
    {
        'input': "Can you show me the records?",
        'description': "Query is ambiguous due to lack of specific details about what data to retrieve"
    },
    {
        'input': "I want to see the number of hits, but when exactly?",
        'description': "Query lacks a specific time frame for data retrieval"
    },
    {
        'input': "How many leads do we have in which industry?",
        'description': "Query is partially complete but missing information about which industry"
    },
    {
        'input': "What is the capital of France?",
        'description': "Query is unrelated to the database and pertains to general knowledge"
    },
    {
        'input': "Can you tell me the latest stock prices?",
        'description': "Query asking for information not contained within the database"
    },
    {
        'input': "What should I have for dinner tonight?",
        'description': "Query seeking personal advice, irrelevant to database querying"
    },
    {
        'input': "Tell me something about our website data.",
        'description': "Query is too broad and lacks specificity about the data required"
    },
    {
        'input': "Can you give me some statistics from the data?",
        'description': "Query lacks specific metrics or dimensions to focus on"
    },
    {
        'input': "What can you show me about our customers?",
        'description': "Query is general and does not define a clear objective or data point"
    }
]


def check(value, expected, info=''):
    assert value == expected, info


def test_accuracy():
    model = create_model()
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

    i = 1
    for testcase in testcases[2:]:
        user_input = testcase['input']
        is_final_output = model.predict(user_input).is_final_output
        check(is_final_output, False, testcase['description'])
        i += 1
        print(f'{i}/{len(testcases)}')