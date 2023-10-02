# Working with python
---
## Extract Data from JSONL to Excel 
## Libraries Used
This Python script extracts data from a JSONL file and creates an Excel file with selected attributes. It uses the argparse library for command-line argument handling and the pandas library for working with data in DataFrames.

- Imports necessary libraries: json, os, pandas (as pd), and argparse.
- Creates an ArgumentParser object (parser) to parse command-line arguments.
- Defines several command-line arguments such as input directory (--input-dir), output directory (--output-dir), language code (--language), and a verbose mode flag (--verbose).
- Parses the command-line arguments and stores their values in corresponding variables (input_dir, output_dir, language, verbose).
- Creates the output directory (output_dir) if it doesn't already exist.
- Iterates through each file in the input directory (input_dir) and selects files with a .jsonl extension.
- For each selected JSONL file, it reads the file, extracts specific attributes (id, utt, annot_utt) from the JSON data, and filters records based on the specified language code (language).
- We then creates a Pandas DataFrame (selected_data) to store the filtered data.
- Determines the output filename based on the input JSONL filename, appends the language code, and changes the extension to .xlsx.
- Writes the selected and filtered data to an Excel file in the output directory.

### main.py
```python
import json
import os
import pandas as pd
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process JSONL files and save relevant data to Excel files.')

# Add flags and arguments
parser.add_argument('--input-dir', '-i', type=str, default='./data/dataset', help='Directory containing JSONL files')
parser.add_argument('--output-dir', '-o', type=str, default='./outputs', help='Output directory for Excel files')
parser.add_argument('--language', '-l', type=str, default='en', help='Language code to filter JSONL files')
parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose mode')

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the flags and arguments
input_dir = args.input_dir
output_dir = args.output_dir
language = args.language
verbose = args.verbose

# Create the output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through each JSONL file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith('.jsonl'):
        file_path = os.path.join(input_dir, filename)

        # Create an empty DataFrame to store the relevant data
        selected_data = pd.DataFrame(columns=['id', 'utt', 'annot_utt'])

        # Read the JSONL file and extract relevant attributes
        with open(file_path, 'r') as json_file:
            data = [json.loads(line) for line in json_file]
            for record in data:
                # Extract the language code from the "locale" attribute
                locale = record.get('locale', '')
                language_code = locale.split('-')[0] if locale else ''

                # Filter records for the specified language code
                if language_code == language:
                    selected_data = pd.concat([selected_data, pd.DataFrame({
                        'id': [record.get('id', '')],
                        'utt': [record.get('utt', '')],
                        'annot_utt': [record.get('annot_utt', '')]
                    })], ignore_index=True)

        # Determine the output filename based on the input JSONL filename
        output_filename = os.path.splitext(language + filename)[0] + '.xlsx'
        output_file = os.path.join(output_dir, output_filename)

        # Write the selected data to an Excel file
        selected_data.to_excel(output_file, index=False)

        if verbose:
            print(f"Processed {filename} and saved as {output_filename}")

print("Excel files generated for each JSONL file and stored in the 'outputs'")
```
