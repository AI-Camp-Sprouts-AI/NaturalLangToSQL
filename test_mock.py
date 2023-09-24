import json
import random
import pytest

# Load JSON file containing the sample data
with open('sample_data.json') as sd:
    data = json.load(sd)

# For now, we will pull the "LLM inputs" from a fixed predefined set of responses
def randomize():
    schema = data['schemas']
    llm_input = random.choice(data['llm_inputs'])
    expected_output = random.choice(data['expected_outputs'])
    return schema, llm_input, expected_output

@pytest.mark.parametrize("schema, llm_input, expected_output", [randomize()])
# Check if the command the LLM gave is correct
# Future: execute LLM input and eval data from DB against expected output
def test_mock(schema, llm_input, expected_output):
    print("LLM Command: " + llm_input)
    print("Expected command: " + expected_output)
    assert llm_input == expected_output

def main():
    schema, llm_input, expected_output = randomize() # honestly not sure if this bit is necessary
    test_mock(schema, llm_input, expected_output)

if __name__ == '__main__':
    pytest.main()