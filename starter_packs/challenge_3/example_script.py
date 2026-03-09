import argparse
import json
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_json',
                        type=Path,
                        default=Path(
                            './test_input_1.json'))  # You can change to test different input data, or provide via CLI
    parser.add_argument('--output_json',
                        type=Path,
                        default=Path(
                            './output.json'))  # You can optionally change the default if you want, or provide via CLI
    args = parser.parse_args()

    with open(args.input_json) as input_file:
        input_data = json.load(input_file)

    n = input_data['n']  # number of Beyeronians
    # Your code goes here

    result = 42  # Replace with your computed result

    with open(args.output_json, 'w') as output_file:
        json.dump({"result": result}, output_file)