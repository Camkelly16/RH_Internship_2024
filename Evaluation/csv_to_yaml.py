import pandas as pd # type: ignore
import yaml
import os

class LiteralString(str):
    pass

def literal_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(LiteralString, literal_str_representer)
yaml.add_representer(LiteralString, yaml.representer.SafeRepresenter.represent_str)

def csv_to_custom_yaml(csv_file_path, yaml_file_path, delimiter=';'):
    # Read the CSV file with the specified delimiter
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    
    # Process the DataFrame to create the required YAML structure
    seed_examples = []
    for _, row in df.iterrows():
        options = [
            f"A) {row['Option A']}",
            f"B) {row['Option B']}",
            f"C) {row['Option C']}",
            f"D) {row['Option D']}"
        ]
        options_text = "\n\n".join(options)
        question_text = f"{row['Question']}\n\n{options_text}"
        correct_answer_letter = chr(65 + (int(row["Correct Answer"]) - 1))  # Convert number to corresponding letter (0 -> A, 1 -> B, etc.)
        correct_answer_text = row[f"Option {correct_answer_letter}"]
        qna_entry = {
            "question": LiteralString(f"{row['Question']}\n\nA) {row['Option A']}\n\nB) {row['Option B']}\n\nC) {row['Option C']}\n\nD) {row['Option D']}"),
            "answer": f"{correct_answer_letter}) {correct_answer_text}"
        }
        seed_examples.append(qna_entry)
    
    # Define the complete YAML structure
    yaml_data = {
        "created_by": "Cameron K",
        "domain": "PromQL",
        "seed_examples": seed_examples,
        "task_description": "Pick the correct answer choice for each PromQL Question"
    }
    
    # Write the YAML data to a file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)
        
    print(f"CSV file '{csv_file_path}' has been converted to YAML file '{yaml_file_path}'")

# Define the file paths
csv_file_path = '/home/cakelly/Desktop/RH_Internship_2024/Datasets/syntax.csv'
yaml_file_path = '/home/cakelly/instructlab/taxonomy/knowledge/PromQL/PromQL.yaml'

# Ensure the output directory exists
os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)

# Convert the CSV to custom YAML
csv_to_custom_yaml(csv_file_path, yaml_file_path)
