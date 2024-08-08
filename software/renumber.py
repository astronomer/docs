#!/usr/bin/env python
import re

def renumber_steps(file_path):
    step_counter = 1

    def transform_line(line):
        nonlocal step_counter
        # Match headers that start with "Step:"
        if re.match(r'^## Step \d+:', line):
            # Replace the current step number with the new step number
            transformed_line = re.sub(r'Step \d+:', f'Step {step_counter}:', line)
            step_counter += 1
            return transformed_line
        else:
            return line

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            transformed_line = transform_line(line)
            file.write(transformed_line)

# read file path from args using argparse
import argparse
parser = argparse.ArgumentParser(description='Renumber steps in a markdown file')
parser.add_argument('file_path', type=str, help='The path to the markdown file')
args = parser.parse_args()
file_path = args.file_path


renumber_steps(file_path)

