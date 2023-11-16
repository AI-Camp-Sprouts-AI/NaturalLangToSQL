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
        'input': "Can you show me the records?",
        'description': "Query is ambiguous due to lack of specific details about what data to retrieve"
    },
    {
        'input': "I want to see the number of hits between X and Y?",
        'description': "Query lacks a specific time frame for data retrieval"
    },
    {
        'input': "How many leads do we have in _ industry?",
        'description': "Query is partially complete but missing information about which industry"
    }
]


def check(value, expected, info=''):
    assert value == expected, info


def test_accuracy():
    model = create_model()
    schema_path = '../../data/schemas/website_aggregates.txt'
    schema_path = CWD.joinpath(schema_path).absolute()
    model.load_schema_from_file(schema_path)

    i = 0
    for testcase in testcases[0:]:
        user_input = testcase['input']
        response = model.predict(user_input)
        content = response.message
        is_final_output = response.is_final_output
        #check(is_final_output, False, testcase['description'] + content)
        if is_final_output == True:
            print("Failed: " + testcase['description'])
        i += 1
        print(f'{i}/{len(testcases)}')