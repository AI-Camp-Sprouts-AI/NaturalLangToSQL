import json
from pprint import pprint

with open('sample_data.json') as sd:
    data = json.load(sd)
    pprint(data)

#def mock_test(schema, input):
#    return