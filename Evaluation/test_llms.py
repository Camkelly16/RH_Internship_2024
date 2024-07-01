import os
#allows os to read and write to the file system
import pandas as pd
#allows for csv file to be read
import argparse
#allows for parsing command-line arguments
from ollama import Client
#allow for me interact with my LLM server 
from deepeval.models.base_model import DeepEvalBaseLLM
#requreiments for me to using Deepeval
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.dataset import EvaluationDataset
from deepeval import evaluate
import logging
#helps with debugging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Ollama(DeepEvalBaseLLM):
    def __init__(self, client, model_name):
        self.model_client = client
        self.model_name = model_name
        #Initializes the class with a client object and a model_name.

    def load_model(self):
        return self.model_client
        #The load_model method returns the model client.

    def generate(self, message_prompt: str) -> str:
        #Method takes a message prompt and generates a response.
        chat_model = self.load_model()
        messages = [
            {
                "role": "system",
                "content": "The assistant is an expert in PromQL queries which is based on Prometheus and answers the questions diligently. "
                           "It does not interfere with any other topics user mentions and politely refuses to answer. The assistant should "
                           "always maintain a professional tone and avoid discussing personal opinions on politics."
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        response = chat_model.chat(model=self.model_name, messages=messages)
        logger.info(f"Generated response: {response}")
        return response["message"]["content"]
        #system instructions and user prompt, sends it to the model client, logs the response, and returns the content of the response.

    async def a_generate(self, message_prompt: str) -> str:
        #allows me to handle multiple
        chat_model = self.load_model()
        messages = [
            {
                "role": "system",
                "content": "The assistant is an expert in PromQL queries which is based on Prometheus and answers the questions diligently. "
                           "It does not interfere with any other topics user mentions and politely refuses to answer. The assistant should "
                           "always maintain a professional tone and avoid discussing personal opinions on politics."
            },
            {
                "role": "user",
                "content": message_prompt,
            },
        ]
        response = chat_model.chat(model=self.model_name, messages=messages)
        return response["message"]["content"]

    def get_model_name(self) -> str:
        return self.model_name
        #returns the model name

def main(model_name):
    client = Client(host='http://localhost:11434', timeout=140)
    model = Ollama(client=client, model_name=model_name)
    #creates a Client object and an Ollama model object.
    
    evaluation_dataset = EvaluationDataset()
    #creates an EvaluationDataset object to hold test cases.
    csv_file_path = os.path.join(os.path.dirname(__file__), '../datasets/sample.csv')
    #the path to the dataset CSV file.

    try:
        df = pd.read_csv(csv_file_path, delimiter=';')
    except FileNotFoundError:
        logger.error(f"Error: The file {csv_file_path} was not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        logger.error(f"Error: The file {csv_file_path} is empty.")
        exit(1)
    except pd.errors.ParserError:
        logger.error(f"Error: The file {csv_file_path} is not a valid CSV file.")
        exit(1)
        #Reads the CSV file and handles potential errors.

    for _, row in df.iterrows():
        question = row['Question']
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        prompt = f"""
        Question:
        {question}
        Only output the content of the correct option and no other information
        -----------
        Options:
        A. {row['Option A']}
        B. {row['Option B']}
        C. {row['Option C']}
        D. {row['Option D']}
        """
        actual_output = model.generate(prompt).strip()

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
        #iterates over the rows, 
        # constructs the prompt, 
        # generates the model's output, 
        # creates and adds test cases to the evaluation dataset.

    metrics = [
        AnswerRelevancyMetric(model=model, threshold=0.5),
        FaithfulnessMetric(model=model, threshold=0.5)
    ]   #the metrics to be used for evaluation.

    evaluate(test_cases=evaluation_dataset, metrics=metrics, run_async=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate LLM with different models.')
    parser.add_argument('--model', type=str, required=True, help='Name of the LLM model to use.')
    #Evaluates the model using the test cases and metrics.
    
    args = parser.parse_args()
    main(args.model)
    #allow of argument parsing for the script, 
    # parsing the --model argument and passing it to the main function.
    # python3 test_llms.py --model llama3
