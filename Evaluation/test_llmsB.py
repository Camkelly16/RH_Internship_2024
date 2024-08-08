import os
import pandas as pd # type: ignore
import argparse
import logging
from ollama import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Ollama:
    def __init__(self, client: Client, model_name: str):
        self.model_client = client
        self.model_name = model_name

    def load_model(self) -> Client:
        return self.model_client

    def generate(self, message_prompt: str) -> str:
        chat_model = self.load_model()
        examples = (
            "You are a PromQl expert taking a PromQl multiple-choice test.\n"
            "For each question, you need to select the correct option from the choices given.\n"
            "Do not provide explanations or additional information.\n\n"
            "### EXAMPLES:\n"
            "### QUESTION:\n"
            "What PromQL expression calculates the rate of HTTP requests over the last 1 minute?\n"
            "### OPTIONS:\n"
            "A. rate(http_requests_total[1m])\n"
            "B. increase(http_requests_total[1m])\n"
            "C. sum(http_requests_total[1m])\n"
            "D. avg(http_requests_total[1m])\n"
            "### ANSWER:\n"
            "A\n\n"
            "### QUESTION:\n"
            "How do you filter metrics by the label 'job' with the value 'api-server'?\n"
            "### OPTIONS:\n"
            "A. http_requests_total{job=\"api-server\"}\n"
            "B. http_requests_total[job=\"api-server\"]\n"
            "C. http_requests_total(job=\"api-server\")\n"
            "D. http_requests_total@job=\"api-server\"\n"
            "### ANSWER:\n"
            "A\n\n"
            "### QUESTION:\n"
            "What is the correct PromQL query to select the CPU time in nanoseconds for a web process in a production environment for a specific application, revision, and job?\n"
            "### OPTIONS:\n"
            "A. instance_cpu_time_ns{app=\"tiger\", proc=\"db\", rev=\"34d0f99\", env=\"dev\", job=\"cluster-manager\"}\n"
            "B. instance_cpu_time_ns{app=\"lion\", proc=\"web\", rev=\"34d0f99\", env=\"prod\", job=\"cluster-manager\"}\n"
            "C. instance_cpu_time_ns{app=\"lion\", proc=\"web\", rev=\"34d0f99\", env=\"staging\", job=\"manager\"}\n"
            "D. instance_cpu_time_ns{app=\"lion\", proc=\"web\", rev=\"1234abcd\", env=\"prod\", job=\"cluster-manager\"}\n"
            "### ANSWER:\n"
            "B\n\n"
        )

        messages = [
            {
                "role": "system",
                "content": examples
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        try:
            response = chat_model.chat(model=self.model_name, messages=messages)
            # Extract the single letter answer (A, B, C, or D) from the response
            if response and response['message'] and response['message']['content']:
                content = response['message']['content'].strip().upper()
                for letter in ['A', 'B', 'C', 'D']:
                    if letter in content:
                        return letter
            logger.error(f"Failed to extract a valid answer from response: {response['message']['content']}")
            return ""
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ""

    async def a_generate(self, message_prompt: str) -> str:
        chat_model = self.load_model()
        examples = (
            "You are a PromQl expert taking a PromQl multiple-choice test.\n"
            "For each question, you need to select the correct option from the choices given.\n"
            "Do not provide explanations or additional information.\n\n"
            "### EXAMPLES:\n"
            "### QUESTION:\n"
            "What PromQL expression calculates the rate of HTTP requests over the last 1 minute?\n"
            "### OPTIONS:\n"
            "A. rate(http_requests_total[1m])\n"
            "B. increase(http_requests_total[1m])\n"
            "C. sum(http_requests_total[1m])\n"
            "D. avg(http_requests_total[1m])\n"
            "### ANSWER:\n"
            "A\n\n"
            "### QUESTION:\n"
            "How do you filter metrics by the label 'job' with the value 'api-server'?\n"
            "### OPTIONS:\n"
            "A. http_requests_total{job=\"api-server\"}\n"
            "B. http_requests_total[job=\"api-server\"]\n"
            "C. http_requests_total(job=\"api-server\")\n"
            "D. http_requests_total@job=\"api-server\"\n"
            "### ANSWER:\n"
            "A\n\n"
            "### QUESTION:\n"
            "What is the correct PromQL query to select the CPU time in nanoseconds for a web process in a production environment for a specific application, revision, and job?\n"
            "### OPTIONS:\n"
            "A. instance_cpu_time_ns{app=\"tiger\", proc=\"db\", rev=\"34d0f99\", env=\"dev\", job=\"cluster-manager\"}\n"
            "B. instance_cpu_time_ns{app=\"lion\", proc=\"web\", rev=\"34d0f99\", env=\"prod\", job=\"cluster-manager\"}\n"
            "C. instance_cpu_time_ns{app=\"lion\", proc=\"web\", rev=\"34d0f99\", env=\"staging\", job=\"manager\"}\n"
            "D. instance_cpu_time_ns{app=\"lion\", proc=\"web\", rev=\"1234abcd\", env=\"prod\", job=\"cluster-manager\"}\n"
            "### ANSWER:\n"
            "B\n\n"
        )

        messages = [
            {
                "role": "system",
                "content": examples
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        try:
            response = await chat_model.chat(model=self.model_name, messages=messages)
            # Extract the single letter answer (A, B, C, or D) from the response
            if response and response['message'] and response['message']['content']:
                content = response['message']['content'].strip().upper()
                for letter in ['A', 'B', 'C', 'D']:
                    if letter in content:
                        return letter
            logger.error(f"Failed to extract a valid answer from response: {response['message']['content']}")
            return ""
        except Exception as e:
            logger.error(f"Error generating response asynchronously: {e}")
            return ""

    def get_model_name(self) -> str:
        return self.model_name

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

def append_accuracy_to_csv(model_name: str, accuracy: float, csv_file_path: str):
    accuracy_data = pd.DataFrame([{'Model': model_name, 'Accuracy': accuracy}])
    if os.path.exists(csv_file_path):
        accuracy_data.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        accuracy_data.to_csv(csv_file_path, mode='w', header=True, index=False)

def main(model_name: str) -> pd.DataFrame:
    client = Client(host='http://localhost:11434', timeout=180)
    model = Ollama(client=client, model_name=model_name)
    
    csv_file_path = os.path.join(os.path.dirname(__file__), '../Datasets/syntax.csv')
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

        # Log the details
        logger.info(f"""
        Question {index + 1}:
        {question}
        Options:
        A. {options[0]}
        B. {options[1]}
        C. {options[2]}
        D. {options[3]}
        Correct Answer: {expected_output}
        Model's Answer: {actual_output}
        """)

        new_row = {
            'Model': model_name,
            'Question Number': index + 1,
            'Model Answer': actual_output,
            'Correct': correctness
        }
        results_list.append(new_row)

    results_df = pd.DataFrame(results_list)

    # Calculate accuracy and display it
    accuracy_percentage = calculate_accuracy(results_df, model_name)
    logger.info(f"Accuracy for {model_name}: {accuracy_percentage:.2f}%")

    # Append the accuracy to the CSV file
    accuracy_csv_path = os.path.join(os.path.dirname(__file__), '../Results/accuracy_scoreQPS.csv')
    append_accuracy_to_csv(model_name, accuracy_percentage, accuracy_csv_path)

    return results_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate LLM with different models.')
    parser.add_argument('--model', type=str, required=True, help='Name of the LLM model to use.')
    
    args = parser.parse_args()
    
    # Define the model to evaluate
    model_name = args.model
    
    # Initialize an empty DataFrame to store results
    all_results_df = pd.DataFrame(columns=['Model', 'Question Number', 'Model Answer', 'Correct'])

    # Load existing results if they exist
    results_csv_path = os.path.join(os.path.dirname(__file__), '../Results/resultsQPS.csv')
    if (os.path.exists(results_csv_path)):
        all_results_df = pd.read_csv(results_csv_path)

    # Evaluate the model
    model_results_df = main(model_name)
    all_results_df = pd.concat([all_results_df, model_results_df], ignore_index=True)

    # Save the results to a CSV file
    all_results_df.to_csv(results_csv_path, index=False)
    
    logger.info(f"Results saved to {results_csv_path}")
        # python test_llmsA.py --model mistral
