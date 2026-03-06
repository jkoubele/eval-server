import argparse
import json
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_json',
                        type=Path,
                        default=Path('./test_input_1.json'))
    parser.add_argument('--output_json',
                        type=Path,
                        default=Path('./output.json'))
    args = parser.parse_args()

    with open(args.input_json) as input_file:
        input_data = json.load(input_file)

    # Your code goes here
    # Fibbonaci to generate some example CPU usage
    a = 1
    b = 1    
    for i in range(7_00_000):
        c = b + a
        a = b
        b = c

    result = 11  # Replace with your computed result

    with open(args.output_json, 'w') as output_file:
        json.dump({"result": result}, output_file)
