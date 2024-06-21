import os
import pandas as pd
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
        messages = [
            {
                "role": "system",
                "content": (
                    "The assistant is an expert in PromQL queries which is based on Prometheus and answers the questions diligently. "
                    "It does not interfere with any other topics user mentions and politely refuses to answer. The assistant should "
                    "always maintain a professional tone and avoid discussing personal opinions on politics."
                )
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        try:
            response = chat_model.chat(model=self.model_name, messages=messages)
            logger.info(f"Generated response: {response}")
            return response["message"]["content"].strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ""

    async def a_generate(self, message_prompt: str) -> str:
        chat_model = self.load_model()
        messages = [
            {
                "role": "system",
                "content": (
                    "The assistant is an expert in PromQL queries which is based on Prometheus and answers the questions diligently. "
                    "It does not interfere with any other topics user mentions and politely refuses to answer. The assistant should "
                    "always maintain a professional tone and avoid discussing personal opinions on politics."
                )
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        try:
            response = await chat_model.chat(model=self.model_name, messages=messages)
            return response["message"]["content"].strip()
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

def main(model_name: str):
    client = Client(host='http://localhost:11434', timeout=140)
    model = Ollama(client=client, model_name=model_name)
    
    csv_file_path = os.path.join(os.path.dirname(__file__), '../datasets/syntax.csv')
    df = read_csv_file(csv_file_path)

    correct_count = 0
    total_count = len(df)

    for _, row in df.iterrows():
        question = row['Question']
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        prompt = create_prompt(question, options)
        actual_output = model.generate(prompt)

        correct_answer_index = int(row['Correct Answer']) - 1
        expected_output = ['A', 'B', 'C', 'D'][correct_answer_index]

        if actual_output == expected_output:
            correct_count += 1
            logger.info(f"Correct: {question}")
        else:
            logger.info(f"Incorrect: {question} - Expected {expected_output}, but got {actual_output}")

    total_score = (correct_count / total_count) * 100
    logger.info(f"Total Score for model {model_name}: {correct_count}/{total_count} ({total_score:.2f}%)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate LLM with different models.')
    parser.add_argument('--model', type=str, required=True, help='Name of the LLM model to use.')
    
    args = parser.parse_args()
    main(args.model)
