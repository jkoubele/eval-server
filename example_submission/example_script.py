import json
import time


with open('./input_data.json') as input_file:
    input_data = json.load(input_file)
    
result = input_data['a'] + input_data['b']
time.sleep(1.0)

with open('./example_output.json', 'w') as output_file:
    json.dump({'result': result}, output_file)

