import pandas as pd
import json
import os

# Define the paths to the JSONL files
en_train_file = 'output_jsonl/en-train.jsonl'
sw_train_file = 'output_jsonl/sw-train.jsonl'
de_train_file = 'output_jsonl/de-train.jsonl'

# Read the JSONL files into DataFrames, selecting only 'id' and 'utt' columns
en_train_df = pd.read_json(en_train_file, lines=True)[['id', 'utt']]
sw_train_df = pd.read_json(sw_train_file, lines=True)[['id', 'utt']]
de_train_df = pd.read_json(de_train_file, lines=True)[['id', 'utt']]

# Merge DataFrames based on 'id'
merged_df = en_train_df.merge(sw_train_df, on='id', suffixes=('_en', '_sw'))
merged_df = merged_df.merge(de_train_df, on='id', suffixes=('_en', '_de'))

# Rename columns to match the desired format
merged_df = merged_df.rename(columns={'utt_en': 'en', 'utt_sw': 'sw', 'utt': 'de'})

# Save the merged DataFrame to a JSONL file with pretty printing
output_file = 'merged_data.jsonl'
with open(output_file, 'w', encoding='utf-8') as jsonl_output_file:
    jsonl_output_file.write(merged_df.to_json(orient='records', lines=True, indent=2))

print("Data merged and saved to 'merged_data.jsonl' with pretty printing")

