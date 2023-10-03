#!/bin/bash

# Default values for flags
input_dir='dataset/mydataset'
output_dir='outputs'

# Define flags and their default values
while getopts "i:o:" opt; do
    case $opt in
        i) input_dir="$OPTARG";;
        o) output_dir="$OPTARG";;
        \?) echo "Invalid option: -$OPTARG" >&2; exit 1;;
    esac
done

# Loop through each JSONL file in the input directory
for filename in "$input_dir"/*.jsonl; do
    if [ -f "$filename" ]; then
        # Determine the output filename based on the input JSONL filename
        output_filename=$(basename -- "$filename" .jsonl).xlsx
        output_file="$output_dir/$output_filename"

        # Call the Python script with flags to extract data and create an Excel file
        python main.py --input "$filename" --output "$output_file"

        echo "Processed $filename and created $output_file"
    fi
done

echo "Excel files generated for each JSONL file and stored in the 'outputs'"
