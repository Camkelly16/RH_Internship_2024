import pandas as pd
import os

def get_correct_answers(syntax_csv_path: str):
    try:
        syntax_df = pd.read_csv(syntax_csv_path, delimiter=';')
    except FileNotFoundError:
        print(f"Error: The file {syntax_csv_path} does not exist.")
        return None, None
    correct_answers = {}
    questions = {}
    for index, row in syntax_df.iterrows():
        question_number = index + 1  # Assuming the index + 1 is the question number
        questions[question_number] = {
            'Question': row['Question'],
            'Option A': row['Option A'],
            'Option B': row['Option B'],
            'Option C': row['Option C'],
            'Option D': row['Option D'],
        }
        correct_option = row['Correct Answer']
        # Map 1, 2, 3, 4 to A, B, C, D
        correct_answer = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}.get(correct_option, None)
        correct_answers[question_number] = correct_answer
    return correct_answers, questions

def organize_results_side_by_side(results_csv_path: str, syntax_csv_path: str, output_csv_path: str, incorrect_csv_path: str):
    # Read the correct answers and questions from syntax.csv
    correct_answers, questions = get_correct_answers(syntax_csv_path)
    if correct_answers is None or questions is None:
        print("Error in getting correct answers or questions.")
        return

    # Read the existing results CSV
    if not os.path.exists(results_csv_path):
        print(f"Error: The file {results_csv_path} does not exist.")
        return
    
    results_df = pd.read_csv(results_csv_path)
    print("Results CSV Columns:", results_df.columns)  # Debug: Print the columns of the results CSV

    # Filter out the actual results rows
    results_df = results_df.dropna(subset=['Question Number'])

    # Create a list to store organized results
    organized_data = []
    incorrect_data = []

    # Get unique question numbers and models
    question_numbers = sorted(results_df['Question Number'].unique())
    models = results_df['Model'].unique()

    # Iterate over each model
    for model in models:
        model_data = results_df[results_df['Model'] == model]
        for question_number in question_numbers:
            question_data = model_data[model_data['Question Number'] == question_number]
            if not question_data.empty:
                answers = question_data['Model Answer'].tolist()
                correct_answer = correct_answers.get(question_number, "No correct answer")
                question_info = questions.get(question_number, {})
                entry = [model, question_number, question_info.get('Question'), 
                         question_info.get('Option A'), question_info.get('Option B'), 
                         question_info.get('Option C'), question_info.get('Option D'), 
                         correct_answer] + answers
                organized_data.append(entry)

                # Check if the model got the answer wrong
                if correct_answer not in answers:
                    incorrect_data.append(entry)

    # Determine the maximum number of answers any model has provided for a question
    max_answers = max(len(row) - 8 for row in organized_data)  # Subtract 8 for fixed columns before the answers

    # Construct columns based on the maximum number of answers
    columns = ['Model', 'Question Number', 'Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer'] + [f'Answer Instance {i+1}' for i in range(max_answers)]

    # Adjust organized_data entries to match the number of columns
    for entry in organized_data:
        if len(entry) < len(columns):
            entry.extend([None] * (len(columns) - len(entry)))

    # Adjust incorrect_data entries to match the number of columns
    for entry in incorrect_data:
        if len(entry) < len(columns):
            entry.extend([None] * (len(columns) - len(entry)))

    # Convert the organized data to a DataFrame
    organized_df = pd.DataFrame(organized_data, columns=columns)
    incorrect_df = pd.DataFrame(incorrect_data, columns=columns)
    
    # Save the organized results to a new CSV file
    organized_df.to_csv(output_csv_path, index=False)
    print(f"Organized results saved to {output_csv_path}")

    # Save the incorrect results to a new CSV file with a semicolon delimiter
    incorrect_df.to_csv(incorrect_csv_path, index=False, sep=';')
    print(f"Incorrect results saved to {incorrect_csv_path}")

if __name__ == "__main__":
    # Define the absolute paths for the input and output files
    results_csv_path = os.path.abspath('Results/resultsNQNP.csv')
    syntax_csv_path = os.path.abspath('Datasets/syntax.csv')
    output_csv_path = os.path.abspath('Results/organized_resultsNQNP.csv')
    incorrect_csv_path = os.path.abspath('Results/incorrectResultsNQNP.csv')
    
    # Debug: Print the file paths being used
    print(f"Results CSV Path: {results_csv_path}")
    print(f"Syntax CSV Path: {syntax_csv_path}")
    print(f"Output CSV Path: {output_csv_path}")
    print(f"Incorrect CSV Path: {incorrect_csv_path}")

    # Organize the results
    organize_results_side_by_side(results_csv_path, syntax_csv_path, output_csv_path, incorrect_csv_path)
