import os
import pandas as pd
import re
from ollama import Client
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.dataset import EvaluationDataset
import json

class Llama3(DeepEvalBaseLLM):
    def __init__(self, client):
        self.client = client

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        client = self.load_model()
        try:
            response = client.chat(model='llama3', messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except Exception as e:
            return f"An error occurred: {e}"

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "Llama3"

def extract_correct_option(output):
    match = re.search(r"The correct answer is ([A-D])\.", output)
    if match:
        return match.group(1)
    match = re.search(r"The correct answer is ([A-D])", output)
    if match:
        return match.group(1)
    return "Invalid Answer"

client = Client(host='http://localhost:11434', timeout=140)
llama3 = Llama3(client=client)
sample = EvaluationDataset()
csv_file_path = os.path.join(os.path.dirname(__file__), '../datasets/sample.csv')

try:
    df = pd.read_csv(csv_file_path, delimiter=';')
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: The file {csv_file_path} is empty.")
    exit(1)
except pd.errors.ParserError:
    print(f"Error: The file {csv_file_path} is not a valid CSV file.")
    exit(1)

for _, row in df.iterrows():
    question = row['Question']
    options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
    prompt = f"{question}\nOptions:\nA. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}"
    actual_output = llama3.generate(prompt)
    actual_output_cleaned = extract_correct_option(actual_output)
    actual_answer_text = options[ord(actual_output_cleaned) - ord('A')] if actual_output_cleaned != "Invalid Answer" else "Invalid Answer"
    correct_answer_index = int(row['Correct Answer']) - 1
    expected_output = options[correct_answer_index]

    test_case = LLMTestCase(
        input=question,
        actual_output=actual_answer_text,
        expected_output=expected_output,
        context=None,
        retrieval_context=[expected_output]
    )
    sample.add_test_case(test_case)

def evaluate_dataset(dataset):
    for test_case in dataset.test_cases:
        relevancy_metric = AnswerRelevancyMetric(model=llama3, threshold=0.5)
        try:
            relevancy_metric.measure(test_case)
        except ValueError as e:
            relevancy_score = f"ValueError: {e}"
        except Exception as e:
            relevancy_score = f"Error: {e}"
        else:
            relevancy_score = relevancy_metric.score

        try:
            faithfulness_metric = FaithfulnessMetric(model=llama3, threshold=0.5)
            faithfulness_metric.measure(test_case)
        except KeyError as e:
            faithfulness_score = f"KeyError: {e}"
        except ValueError as e:
            faithfulness_score = f"ValueError: {e}"
        except Exception as e:
            faithfulness_score = f"Error: {e}"
        else:
            faithfulness_score = faithfulness_metric.score

        print(f"Actual Answer: {test_case.actual_output}")
        print(f"Expected Answer: {test_case.expected_output}")
        print(f"Relevancy Score: {relevancy_score}")
        print(f"Faithfulness Score: {faithfulness_score}")
        print("-" * 20)

evaluate_dataset(sample)