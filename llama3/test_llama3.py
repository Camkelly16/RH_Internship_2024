import json
from ollama import Client  # type: ignore
from deepeval.models.base_model import DeepEvalBaseLLM  # type: ignore
from deepeval.test_case import LLMTestCase  # type: ignore
from deepeval.metrics.base_metric import BaseMetric  # type: ignore
from deepeval.dataset import EvaluationDataset  # type: ignore

class Llama3(DeepEvalBaseLLM):
    def __init__(self, client):
        self.client = client

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        client = self.load_model()
        try:
            response = client.chat(model='llama3', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            return response['message']['content']
        except Exception as e:
            return f"An error occurred: {e}"

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "Llama 3"

# Custom relevancy metric class
class CustomAnswerRelevancyMetric(BaseMetric):
    def __init__(self, model, threshold=0.5):
        self.model = model
        self.threshold = threshold
        self.score = 0
        self.reason = ""

    def measure(self, test_case: LLMTestCase):
        prompt = f"Is the following answer relevant to the question?\n\nQuestion: {test_case.input}\nAnswer: {test_case.actual_output}\nExpected: {test_case.expected_output}"
        response = self.model.generate(prompt)
        self.score = 1 if "yes" in response.lower() else 0
        self.reason = response

# Custom faithfulness metric class
class CustomFaithfulnessMetric(BaseMetric):
    def __init__(self, model, threshold=0.5):
        self.model = model
        self.threshold = threshold
        self.score = 0
        self.reason = ""

    def measure(self, test_case: LLMTestCase):
        prompt = f"Is the following answer faithful to the information in the question?\n\nQuestion: {test_case.input}\nAnswer: {test_case.actual_output}"
        response = self.model.generate(prompt)
        self.score = 1 if "yes" in response.lower() else 0
        self.reason = response

# Create a custom client with specified host and timeout
client = Client(host='http://localhost:11434', timeout=100)
llama_3 = Llama3(client=client)

# Add your dataset
sample = EvaluationDataset()

# Assuming your JSON file path is '../datasets/sample.json'
json_file_path = "../datasets/sample.json"

# Load the dataset from the JSON file
try:
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON file.")
    exit(1)

# Add test cases to the dataset
for item in json_data:
    question = item['Question']
    options = [
        item['Option A'],
        item['Option B'],
        item['Option C'],
        item['Option D']
    ]
    correct_answer_index = item['Correct Answer'] - 1  # Adjust for 0-based index
    correct_answer = options[correct_answer_index]
    
    # Create the prompt for the model
    prompt = f"{question}\nA. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}\nChoose the correct answer (A, B, C, or D):"
    
    # Generate the response from the model
    actual_output = llama_3.generate(prompt)
    
    # Convert the model's response to the actual answer text
    actual_output_cleaned = actual_output.strip().upper()
    if actual_output_cleaned in ['A', 'B', 'C', 'D']:
        actual_answer_text = options[ord(actual_output_cleaned) - ord('A')]
    else:
        # Attempt to map a text answer to one of the options
        actual_answer_text = "Invalid Answer"
        for key, value in {'A': options[0], 'B': options[1], 'C': options[2], 'D': options[3]}.items():
            if value.strip().lower() in actual_output.strip().lower():
                actual_answer_text = value
                break

    # Create the test case
    test_case = LLMTestCase(
        input=question,
        actual_output=actual_answer_text,
        expected_output=correct_answer,
        context=None,  # Set to None if no context is available
        retrieval_context=None  # Set to None if no retrieval context is available
    )
    sample.add_test_case(test_case)

# Function to measure and print metrics for the dataset
def evaluate_dataset(dataset):
    for test_case in dataset.test_cases:
        # Measure the relevancy of the generated response using the custom metric
        relevancy_metric = CustomAnswerRelevancyMetric(model=llama_3, threshold=0.5)
        relevancy_metric.measure(test_case)
        print(f"Question: {test_case.input}")
        print(f"Actual Answer: {test_case.actual_output}")
        print(f"Expected Answer: {test_case.expected_output}")
        print(f"Relevancy Score: {relevancy_metric.score} (Good)" if relevancy_metric.score == 1 else f"Relevancy Score: {relevancy_metric.score} (Not good)")
        print(f"Reason (Relevancy): {relevancy_metric.reason}")

        # Measure faithfulness of the generated response using the custom metric
        faithfulness_metric = CustomFaithfulnessMetric(model=llama_3, threshold=0.5)
        faithfulness_metric.measure(test_case)
        print(f"Faithfulness Score: {faithfulness_metric.score} (Good)" if faithfulness_metric.score == 1 else f"Faithfulness Score: {faithfulness_metric.score} (Not good)")
        print(f"Reason (Faithfulness): {faithfulness_metric.reason}")
        print("-" * 20)

# Evaluate the dataset
evaluate_dataset(sample)
