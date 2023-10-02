import json
import os

# Define the input directory containing the original JSONL files
input_dir = 'dataset/data'

# Define the output directory where the separated JSONL files will be saved
output_dir = 'output_jsonl'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the languages and partitions
languages = ['en', 'sw', 'de']
partitions = ['test', 'train', 'dev']

# Loop through each language and partition
for lang in languages:
    for partition in partitions:
        # Define the output JSONL file name
        output_file_name = f'{lang}-{partition}.jsonl'
        output_file_path = os.path.join(output_dir, output_file_name)

        # Create an empty list to store records for the current language and partition
        records = []

        # Loop through the original JSONL files
        for filename in os.listdir(input_dir):
            if filename.endswith('.jsonl'):
                file_path = os.path.join(input_dir, filename)

                with open(file_path, 'r', encoding='utf-8') as jsonl_file:
                    lines = jsonl_file.readlines()
                    for line in lines:
                        data = json.loads(line)
                        # Check if the data matches the current language and partition
                        if data.get('locale', '').startswith(lang) and data.get('partition') == partition:
                            records.append(data)

        # Write the selected records to the output JSONL file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for record in records:
                json.dump(record, output_file, ensure_ascii=False)
                output_file.write('\n')

        print(f'Generated {output_file_name}')

print('Separate JSONL files generated for each language and partition.')