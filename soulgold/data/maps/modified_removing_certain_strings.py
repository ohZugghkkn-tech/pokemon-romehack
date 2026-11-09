import os
import re

def remove_lines(input_file, output_file, pattern):
    # Compile the regular expression pattern for matching lines to remove
    regex = re.compile(pattern)

    # Open the input file for reading
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Open the output file for writing
    with open(output_file, 'w') as outfile:
        for line in lines:
            # If the line matches the pattern, skip it
            if not regex.match(line):
                outfile.write(line)

def process_directory(root_dir, pattern):
    # Walk through the directory and process all Python files
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):  # Only process Python files
                input_file = os.path.join(dirpath, filename)
                output_file = os.path.join(dirpath, f"modified_{filename}")  # Add a prefix to output file name

                # Call remove_lines for each Python file
                remove_lines(input_file, output_file, pattern)
                print(f"Processed {input_file} -> {output_file}")

# Example usage
root_dir = 'C:\decomps\HNSPort\data\maps'  # Replace with the root directory path
pattern = r'^\s*register_matchcall'  # Pattern to remove lines starting with "register_matchcall"

process_directory(root_dir, pattern)
