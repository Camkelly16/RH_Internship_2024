import os
import logging
import pandas as pd # type: ignore
import requests
import warnings
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint # type: ignore

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
        endpoint_url = "https://granite-7b-instruct-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com/"
        #https://granite-7b-instruct-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com/
        #https://mistral-7b-instruct-v03-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com/
        #http://meta-llama3-8b-instruct-perfconf-hackathon.apps.dripberg-dgx2.rdu3.labs.perfscale.redhat.com/
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
        # Define the prompt template with the provided few-shot examples
        few_shot_examples = """
        You are a PromQl expert taking a PromQl multiple-choice test.
        For each question, you need to select the correct option from the choices given.
        Do not provide explanations or additional information.

        ### EXAMPLES:
        ### QUESTION:
        What PromQL expression calculates the rate of HTTP requests over the last 1 minute?
        ### OPTIONS:
        A. rate(http_requests_total[1m])
        B. increase(http_requests_total[1m])
        C. sum(http_requests_total[1m])
        D. avg(http_requests_total[1m])
        ### ANSWER:
        A

        ### QUESTION:
        How do you filter metrics by the label 'job' with the value 'api-server'?
        ### OPTIONS:
        A. http_requests_total{job="api-server"}
        B. http_requests_total[job="api-server"}
        C. http_requests_total(job="api-server")
        D. http_requests_total@job="api-server"
        ### ANSWER:
        A

        ### QUESTION:
        What is the correct PromQL query to select the CPU time in nanoseconds for a web process in a production environment for a specific application, revision, and job?
        ### OPTIONS:
        A. instance_cpu_time_ns{app="tiger", proc="db", rev="34d0f99", env="dev", job="cluster-manager"}
        B. instance_cpu_time_ns{app="lion", proc="web", rev="34d0f99", env="prod", job="cluster-manager"}
        C. instance_cpu_time_ns{app="lion", proc="web", rev="34d0f99", env="staging", job="manager"}
        D. instance_cpu_time_ns{app="lion", proc="web", rev="1234abcd", env="prod", job="cluster-manager"}
        ### ANSWER:
        B
        """

        # Append the actual question and options to the few-shot examples
        prompt_template = f"""
        {few_shot_examples}

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
    results_csv_path = os.path.join(os.path.dirname(__file__), '../Results/resultsNQPS.csv')
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

    # Log and save accuracy score
    logger.info(f"Accuracy: {accuracy:.2f}%")
    save_accuracy_score("Granite", accuracy)

    print(f"Results saved to {results_csv_path}")
    print(f"Accuracy: {accuracy:.2f}%")

def save_accuracy_score(model_name, accuracy):
    # Path to the accuracy score file
    accuracy_score_file = os.path.join(os.path.dirname(__file__), '../Results/accuracy_scoreNQPS.csv')

    # Check if the file exists
    file_exists = os.path.exists(accuracy_score_file)

    # Create the DataFrame for the new score
    new_score_df = pd.DataFrame([[model_name, accuracy]], columns=["Model", "Accuracy"])

    if file_exists:
        # Load existing scores
        existing_scores_df = pd.read_csv(accuracy_score_file)
        # Append the new score to the existing scores
        updated_scores_df = pd.concat([existing_scores_df, new_score_df], ignore_index=True)
    else:
        # If the file doesn't exist, the updated scores are just the new score
        updated_scores_df = new_score_df

    # Save the updated scores to the CSV file
    updated_scores_df.to_csv(accuracy_score_file, index=False)

if __name__ == "__main__":
    # Construct the full path to the CSV file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_dir, '..', 'Datasets', 'syntax.csv')
    
    # Log the path for debugging
    logger.info(f"CSV file path: {csv_file_path}")

    # Verify the current working directory
    current_working_dir = os.getcwd()
    logger.info(f"Current working directory: {current_working_dir}")

    # Read questions and generate answers
    read_and_generate_answers(csv_file_path)
