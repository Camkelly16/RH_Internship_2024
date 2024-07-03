import os
import logging
import pandas as pd
import requests
import warnings
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

# Ensure the CURL_CA_BUNDLE is empty to avoid SSL issues
os.environ["CURL_CA_BUNDLE"] = ""

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable warnings for requests and other potential warnings
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")

class DGX:
    def __init__(self):
        # Ensure the Hugging Face API key is set correctly
        api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not api_key:
            raise ValueError("Hugging Face API token not set in environment variables.")

        # Set the endpoint URL directly
        endpoint_url = "https://granite-7b-base-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com/"

        # Create a session and disable SSL verification
        session = requests.Session()
        session.verify = False

        # Update the HuggingFaceEndpoint to use the session for requests
        self.llm = HuggingFaceEndpoint(
            endpoint_url=endpoint_url,
            max_new_tokens=512,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            client=session
        )

    def generate(self, options: str, question: str) -> str:
        # Define the prompt template
        prompt_template = f"""
        You are a PromQl expert taking a PromQl multiple-choice test.
        For each question, you need to select the correct option from the choices given.
        Your response should only be the letter of the correct option (A, B, C, or D) and nothing else.
        Do not provide explanations or additional information.

        ### QUESTION: 
        {question}
        ### OPTIONS:
        {options}

        ### ANSWER:
        """
        response = self.llm.invoke(prompt_template)
        # Strip and debug the response
        response = response.strip()
        logger.debug(f"Raw response: {response}")
        # Extract only the first letter if response contains unwanted characters
        if response and len(response) > 0:
            response = response[0]
        return response

def read_and_generate_answers(csv_file_path):
    # Verify if the file exists
    if not os.path.exists(csv_file_path):
        logger.error(f"File not found: {csv_file_path}")
        return

    # Read the CSV file with appropriate delimiter
    df = pd.read_csv(csv_file_path, delimiter=';')
    logger.info(f"CSV columns: {df.columns.tolist()}")

    # Instantiate the DGX class
    dgx = DGX()

    results = []

    total_questions = 0
    correct_answers = 0

    # Mapping from number to letter
    num_to_letter = {
        "1": "A",
        "2": "B",
        "3": "C",
        "4": "D"
    }

    # Initialize an empty DataFrame to store results
    all_results_df = pd.DataFrame(columns=['Model', 'Question Number', 'Model Answer', 'Correct'])

    # Load existing results if they exist
    results_csv_path = os.path.join(os.path.dirname(__file__), '../datasets/resultsNQ.csv')
    if os.path.exists(results_csv_path):
        all_results_df = pd.read_csv(results_csv_path)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        total_questions += 1
        question_number = index + 1
        question = row['Question']
        option_a = row['Option A']
        option_b = row['Option B']
        option_c = row['Option C']
        option_d = row['Option D']
        options = [option_a, option_b, option_c, option_d]
        correct_answer_num = str(row['Correct Answer'])
        correct_answer = num_to_letter.get(correct_answer_num, "")
        generated_answer = dgx.generate(f"A. {option_a}\nB. {option_b}\nC. {option_c}\nD. {option_d}", question)
        
        is_correct = generated_answer == correct_answer
        if is_correct:
            correct_answers += 1

        results.append({
            "Model": "Granite",
            "Question Number": question_number,
            "Model Answer": generated_answer,
            "Correct": is_correct
        })

        # Log the details
        logger.info(f"""
        Question {index + 1}:
        {question}
        Options:
        A. {options[0]}
        B. {options[1]}
        C. {options[2]}
        D. {options[3]}
        Correct Answer: {correct_answer}
        Model's Answer: {generated_answer}
        """)

    # Calculate overall accuracy
    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    # Append new results to the DataFrame
    new_results_df = pd.DataFrame(results)
    all_results_df = pd.concat([all_results_df, new_results_df], ignore_index=True)

    # Save the updated results to the CSV file
    all_results_df.to_csv(results_csv_path, index=False)

    print(f"Results saved to {results_csv_path}")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    # Construct the full path to the CSV file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_dir, '..', 'datasets', 'syntax.csv')
    
    # Log the path for debugging
    logger.info(f"CSV file path: {csv_file_path}")

    # Verify the current working directory
    current_working_dir = os.getcwd()
    logger.info(f"Current working directory: {current_working_dir}")

    # Read questions and generate answers
    read_and_generate_answers(csv_file_path)
