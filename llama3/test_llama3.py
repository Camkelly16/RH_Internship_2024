import os
import pandas as pd
from ollama import Client
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.dataset import EvaluationDataset
from deepeval import evaluate

class OllamaLlama3(DeepEvalBaseLLM):
    def __init__(self, client):
        self.model_client = client

    def load_model(self):
        return self.model_client

    def generate(self, message_prompt: str) -> str:
        chat_model = self.load_model()
        messages = [
            {
                "role": "system",
                "content": "The assistant is an expert in PromQL queries which is based on prometheus and answers the questions diligently, \
                    it does not interfere with any other topics user mentions and politely refuses to answer. The assistant should always maintain a professional tone and avoid discussing personal opinions on politics.",
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        response = chat_model.chat(model="llama3", messages=messages)
        print(response)
        return response["message"]["content"]

    async def a_generate(self, message_prompt: str) -> str:
        chat_model = self.load_model()
        messages = [
            {
                "role": "system",
                "content": "The assistant is an expert in PromQL queries which is based on prometheus and answers the questions diligently, \
                    it does not interfere with any other topics user mentions and politely refuses to answer. The assistant should always maintain a professional tone and avoid discussing personal opinions on politics.",
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        response = chat_model.chat(model="llama3", messages=messages)
        return response["message"]["content"]

    def get_model_name(self) -> str:
        return "Llama3 Ollama"

client = Client(host='http://localhost:11434', timeout=140)
llama3 = OllamaLlama3(client=client)
evaluation_dataset = EvaluationDataset()
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
    prompt = f"""
    Question:
    {question}
    Only output the content of the correct option
    -----------
    Options:
    A. {row['Option A']}
    B. {row['Option B']}
    C. {row['Option C']}
    D. {row['Option D']}
    """
    actual_output = llama3.generate(prompt).strip()
    
    correct_answer_index = int(row['Correct Answer']) - 1
    expected_output = options[correct_answer_index]

    test_case = LLMTestCase(
        input=question,
        actual_output=actual_output,
        expected_output=expected_output,
        context=None,
        retrieval_context=[""]
    )
    evaluation_dataset.add_test_case(test_case)

metrics = [
    AnswerRelevancyMetric(model=llama3, threshold=0.5),
    FaithfulnessMetric(model=llama3, threshold=0.5)
]
evaluate(test_cases=evaluation_dataset, metrics=metrics, run_async=False)
