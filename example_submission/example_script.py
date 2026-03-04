import json
import time


with open('./input_data.json') as input_file:
    input_data = json.load(input_file)
    
result = input_data['a'] + input_data['b']

# Fibbonaci to generate some example CPU usage
a = 1
b = 1
t0 = time.time()
for i in range(1_00_000):
    c = b + a
    a = b
    b = c
    
t1 = time.time()
print(t1-t0)


with open('./example_output.json', 'w') as output_file:
    json.dump({'result': result}, output_file)

