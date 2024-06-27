import os
import logging
import re
import pandas as pd
import argparse
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.huggingface_text_gen_inference import HuggingFaceTextGenInference
import requests
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable warnings
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")

class Llama3:
    def __init__(self):
        server_url = "https://meta-llama3-8b-instruct-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com"
        
        # Create a session and disable SSL verification
        session = requests.Session()
        session.verify = False
        
        self.llm = HuggingFaceTextGenInference(
            inference_server_url=server_url,
            max_new_tokens=512,
            top_k=10,
            top_p=0.5,
            typical_p=0.5,
            temperature=0.05,
            repetition_penalty=1.03,
            streaming=True,
            client=session  # Pass the session with disabled SSL verification
        )

    def generate(self, context: str, question: str) -> str:
        try:
            # Define the prompt template
            prompt_template = """
            You are a PromQl expert taking a PromQl multiple-choice test.
            For each question, you need to select the correct option from the choices given.
            Your response should only be the letter of the correct option (A, B, C, or D) and nothing else.
            Do not provide explanations or additional information.

            Here is the context to consider when answering the question:
            {context}

            ### QUESTION: 
            {question}
            ### ANSWER:
            """

            # Create the prompt template instance
            prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
            llm_chain = LLMChain(llm=self.llm, prompt=prompt)
            response = llm_chain.invoke({"context": context, "question": question})
            logger.info(f"Generated response: {response}")

            # Extract the answer from the response
            if response and response['text']:
                match = re.search(r'\b[A-D]\b', response['text'])
                if match:
                    return match.group(0)
            logger.error(f"Failed to extract a valid answer from response: {response}")
            return ""
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e}")
            return ""

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

def calculate_accuracy(results_df: pd.DataFrame) -> float:
    correct_answers = results_df['Correct'].sum()
    total_questions = len(results_df)
    if total_questions == 0:
        return 0.0
    accuracy_percentage = (correct_answers / total_questions) * 100
    return accuracy_percentage

def main() -> pd.DataFrame:
    model = Llama3()
    
    csv_file_path = os.path.join(os.path.dirname(__file__), '../datasets/sample.csv')
    df = read_csv_file(csv_file_path)

    results_list = []

    for index, row in df.iterrows():
        question = row['Question']
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        prompt = create_prompt(question, options)
        context = f"Options:\nA. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}"
        actual_output = model.generate(context, question)

        correct_answer_index = int(row['Correct Answer']) - 1
        expected_output = ['A', 'B', 'C', 'D'][correct_answer_index]
        correctness = actual_output == expected_output

        new_row = {
            'Model': 'Llama3',
            'Question Number': index + 1,
            'Model Answer': actual_output,
            'Correct': correctness
        }
        results_list.append(new_row)

    results_df = pd.DataFrame(results_list)

    # Calculate accuracy
    accuracy_percentage = calculate_accuracy(results_df)
    logger.info(f"Accuracy: {accuracy_percentage:.2f}%")

    # Add accuracy to the results DataFrame
    accuracy_row = pd.DataFrame([{
        'Model': 'Llama3',
        'Question Number': 'Accuracy',
        'Model Answer': '',
        'Correct': accuracy_percentage
    }])
    results_df = pd.concat([results_df, accuracy_row], ignore_index=True)

    return results_df

if __name__ == "__main__":
    # Initialize an empty DataFrame to store results
    all_results_df = pd.DataFrame(columns=['Model', 'Question Number', 'Model Answer', 'Correct'])

    # Load existing results if they exist
    results_csv_path = os.path.join(os.path.dirname(__file__), '../datasets/Llama3_results.csv')
    if os.path.exists(results_csv_path):
        all_results_df = pd.read_csv(results_csv_path)

    # Evaluate the model
    model_results_df = main()
    all_results_df = pd.concat([all_results_df, model_results_df], ignore_index=True)

    # Save the results to a CSV file
    all_results_df.to_csv(results_csv_path, index=False)
    
    logger.info(f"Results saved to {results_csv_path}")
