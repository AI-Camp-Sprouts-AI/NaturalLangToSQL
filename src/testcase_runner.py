"""
This function has to be used to run the test cases.

This should output benchmarking results ( Like accuracy )

This module should expose functions to
1. Run the test cases

I leave the structure of this module implementation to the developer.
"""

from os import getenv
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from .main import initialize_model
from .test_cases import test_cases
from .database_connector import execute_command
import csv

def run_testcases():
    load_dotenv()
    openai_api_key = getenv('OPENAI_API_KEY')
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",
                     openai_api_key=openai_api_key, temperature=0)
    model = initialize_model(llm=llm, options={'memory': 0, 'review': True})
    
    outputs = []

    i = 0
    passed = 0
    for test_case in test_cases:
        summary = test_case['summary']
        prompt = test_case['prompt']
        schema = test_case['schema']
        correct_query = test_case['correct_query']
        valid_prompt = test_case['valid_prompt']

        model.load_schema_as_string(schema)
        model_response = model.predict(prompt)
        model_query = model_response.message
        model_valid_prompt = model_response.is_final_output

        correct_data = None
        model_data = None
        if valid_prompt and model_valid_prompt:
            try:
                correct_data = execute_command(correct_query)
                model_data = execute_command(model_query)
            except Exception as e:
                correct_data = None
                model_data = None

        test_pass = False
        i += 1
        if (valid_prompt == True and model_valid_prompt == True and correct_data == model_data) or (valid_prompt == False and model_valid_prompt == False):
            passed += 1
            test_pass = True
            print(f"{i}/{len(test_cases)}")
        else:
            print("Failed Test: " + summary)

        if i >= 10:
            break


        outputs.append({
            'pass': test_pass,
            'summary': summary,
            'prompt': prompt,
            'correct_query': correct_query,
            'model_query': model_query,
            'valid_prompt': valid_prompt,
            'model_valid_prompt': model_valid_prompt,
            'correct_query_data': correct_data,
            'model_query_data': model_data
        })

    print(str(passed / len(outputs) * 100) + "% Pass Rate")

    for data in outputs:
        for key in data:
            data[key] = str(data[key])[:1000] if len(str(data[key])) > 1000 else str(data[key])

    with open('tests.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=outputs[0].keys())
        writer.writeheader()
        for data in outputs:
            writer.writerow(data)

    return outputs