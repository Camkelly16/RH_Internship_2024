import pandas as pd
import yaml
import os

def format_question(row):
    question = row["Question"]
    options = f'A) {row["Option A"]}\nB) {row["Option B"]}\nC) {row["Option C"]}\nD) {row["Option D"]}'
    return f"{question}\n{options}"

def format_answer(row):
    answer_map = {
        "1": f'A) {row["Option A"]}',
        "2": f'B) {row["Option B"]}',
        "3": f'C) {row["Option C"]}',
        "4": f'D) {row["Option D"]}'
    }
    return answer_map[str(row["Correct Answer"])]

def csv_to_custom_yaml(csv_file_path, yaml_file_path, delimiter=';'):
    # Read the CSV file with the specified delimiter
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    
    # Process the DataFrame to create a list of QnA objects
    qna_list = []
    for _, row in df.iterrows():
        qna_entry = {
            "question": format_question(row),
            "answer": format_answer(row)
        }
        qna_list.append(qna_entry)
    
    # Write the list to a YAML file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(qna_list, yaml_file, sort_keys=False, default_flow_style=False, width=4096)
        
    print(f"CSV file '{csv_file_path}' has been converted to YAML file '{yaml_file_path}'")

def create_datasets_from_csv():
    # Define file paths for the syntax.csv
    syntax_csv_file_path = 'Datasets/syntax.csv'
    syntax_yaml_file_path = '/home/cakelly/dataset/syntax_train_data.yaml'
    
    # Convert syntax.csv to YAML
    csv_to_custom_yaml(syntax_csv_file_path, syntax_yaml_file_path)

    # Define file paths for the incorrectResultsNQ.csv
    incorrect_csv_file_path = 'Results/incorrectResultsNQ.csv'
    output_dir = '/home/cakelly/dataset'

    # Read the CSV file with the specified delimiter
    df = pd.read_csv(incorrect_csv_file_path, delimiter=';')
    
    # Group the DataFrame by the 'Model' column
    grouped = df.groupby('Model')
    
    # Process each group to create separate YAML files
    for model, group in grouped:
        qna_list = []
        for _, row in group.iterrows():
            qna_entry = {
                "question": format_question(row),
                "answer": format_answer(row)
            }
            qna_list.append(qna_entry)
        
        # Define the output file path
        yaml_file_path = os.path.join(output_dir, f'{model}_train_data.yaml')
        
        # Write the list to a YAML file
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(qna_list, yaml_file, sort_keys=False, default_flow_style=False, width=4096)
        
        print(f"CSV data for model '{model}' has been converted to YAML file '{yaml_file_path}'")

# Ensure the output directory exists
os.makedirs('/home/cakelly/dataset', exist_ok=True)

# Create datasets from CSV
create_datasets_from_csv()
