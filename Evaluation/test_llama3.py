import os
import pandas as pd
import argparse
import logging
import re
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceModel:
    def __init__(self, endpoint_url: str, api_key: str):
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def generate(self, message_prompt: str) -> str:
        payload = {
            "inputs": message_prompt,
            "parameters": {
                "max_new_tokens": 50,  # Adjust as needed
                "return_full_text": False,
                "top_k": 10,
                "top_p": 0.9,
                "temperature": 0.7
            }
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.post(self.endpoint_url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            generated_text = response_json[0]['generated_text']
            logger.info(f"Generated response: {generated_text}")
            # Extract the single letter answer (A, B, C, or D) from the response
            match = re.search(r'\b[A-D]\b', generated_text)
            if match:
                return match.group(0)
            logger.error(f"Failed to extract a valid answer from response: {generated_text}")
            return ""
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ""

    async def a_generate(self, message_prompt: str) -> str:
        return self.generate(message_prompt)  # For simplicity, using the same method synchronously

def read_csv_file(csv_file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(csv_file_path, delimiter=';')
    except FileNotFoundError:
        logger.error(f"Error: The file {csv_file_path} was not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        logger.error(f"Error: The file {csv_file_path} is empty.")
        exit(1)
    except pd.errors.ParserError:
        logger.error(f"Error: The file {csv_file_path} is not a valid CSV file.")
        exit(1)

def create_prompt(question: str, options: list[str]) -> str:
    return f"""
    Question:
    {question}
    Only output the letter of the correct option (A, B, C, or D) without any additional text or explanation.
    -----------
    Options:
    A. {options[0]}
    B. {options[1]}
    C. {options[2]}
    D. {options[3]}
    """

def calculate_accuracy(results_df: pd.DataFrame, model_name: str) -> float:
    model_results = results_df[results_df['Model'] == model_name]
    correct_answers = model_results['Correct'].sum()
    total_questions = len(model_results)
    if total_questions == 0:
        return 0.0
    accuracy_percentage = (correct_answers / total_questions) * 100
    return accuracy_percentage

def main(model_name: str, results_df: pd.DataFrame, endpoint_url: str, api_key: str) -> pd.DataFrame:
    model = HuggingFaceModel(endpoint_url=endpoint_url, api_key=api_key)
    
    csv_file_path = os.path.join(os.path.dirname(__file__), '../datasets/syntax.csv')
    df = read_csv_file(csv_file_path)

    results_list = []

    for index, row in df.iterrows():
        question = row['Question']
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        prompt = create_prompt(question, options)
        actual_output = model.generate(prompt)

        correct_answer_index = int(row['Correct Answer']) - 1
        expected_output = ['A', 'B', 'C', 'D'][correct_answer_index]
        correctness = actual_output == expected_output

        new_row = {
            'Model': model_name,
            'Question Number': index + 1,
            'Model Answer': actual_output,
            'Correct': correctness
        }
        results_list.append(new_row)

    results_df = pd.concat([results_df, pd.DataFrame(results_list)], ignore_index=True)
    
    return results_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate LLM with different models.')
    parser.add_argument('--models', type=str, nargs='+', required=True, help='Names of the LLM models to use.')
    parser.add_argument('--endpoint_url', type=str, required=True, help='Endpoint URL for the HuggingFace model.')
    parser.add_argument('--api_key', type=str, required=True, help='API key for accessing the HuggingFace model.')
    
    args = parser.parse_args()
    
    # Define the list of models to evaluate
    models = args.models
    
    # Initialize an empty DataFrame to store results
    all_results_df = pd.DataFrame(columns=['Model', 'Question Number', 'Model Answer', 'Correct'])

    # Load existing results if they exist
    results_csv_path = os.path.join(os.path.dirname(__file__), '../datasets/results.csv')
    if os.path.exists(results_csv_path):
        all_results_df = pd.read_csv(results_csv_path)

    # Loop through each model and evaluate
    accuracy_scores = []

    for model_name in models:
        all_results_df = main(model_name, all_results_df, args.endpoint_url, args.api_key)
        accuracy_percentage = calculate_accuracy(all_results_df, model_name)
        accuracy_scores.append({'Model': model_name, 'Accuracy': accuracy_percentage})
        logger.info(f"Accuracy for {model_name}: {accuracy_percentage:.2f}%")

    # Convert accuracy scores to DataFrame and append to results
    accuracy_df = pd.DataFrame(accuracy_scores)
    all_results_df = pd.concat([all_results_df, accuracy_df], ignore_index=True)

    # Save the results to a CSV file
    all_results_df.to_csv(results_csv_path, index=False)
    
    logger.info(f"Results saved to {results_csv_path}")
