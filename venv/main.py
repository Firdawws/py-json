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
