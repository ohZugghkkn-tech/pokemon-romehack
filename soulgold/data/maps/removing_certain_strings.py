import os
import re

def remove_lines(input_file, pattern):
    # Compile the regular expression pattern for matching lines to remove
    regex = re.compile(pattern)
    updated_lines = []

    # Open the input file for reading
    with open(input_file, 'r') as infile:
        for line in infile:
            # Only add the line if it does not match the pattern
            if not regex.match(line):
                updated_lines.append(line)

    # Rewrite the file with the updated lines (with the "register_matchcall" lines removed)
    with open(input_file, 'w') as outfile:
        outfile.writelines(updated_lines)

def process_directory(root_dir, pattern):
    # Walk through the directory and its subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Only process the scripts.inc file
            if filename == 'scripts.inc':
                input_file = os.path.join(dirpath, filename)
                print("Processing file: {}".format(input_file))

                # Call remove_lines for each scripts.inc file
                remove_lines(input_file, pattern)

# Example usage
root_dir = 'C:\decomps\HNSPort\data\maps'  # Replace with the root directory path
pattern = r'^\s*register_matchcall'  # Pattern to remove lines starting with "register_matchcall"

process_directory(root_dir, pattern)
