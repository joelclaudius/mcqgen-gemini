import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file: " + str(e))

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format. Only PDF and text files are supported.")

def get_table_data(quiz_str):
    if not quiz_str or not isinstance(quiz_str, str):
        print("Invalid quiz string provided.")
        return []

    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        for key, value in quiz_dict.items():
            quiz_table_data.append({
                "Question": value["mcq"],
                "Options": ', '.join(value["options"]),  # Joining options for display
                "Correct Answer": value["correct"]
            })
        return quiz_table_data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return []
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return []

def load_quiz_data(quiz_json):
    """Load quiz data from a JSON string."""
    return json.loads(quiz_json)

def calculate_score(results):
    """Calculate the user's score based on their answers."""
    score = 0
    for _, user_answer, correct_answer, _ in results:
        if user_answer == correct_answer:
            score += 1
    return score

def display_question(question_data, question_key):
    """Display a question and its options."""
    question_text = question_data['mcq']
    options = question_data['options']
    
    return question_text, options

def display_results(total_score, total_questions, results, quiz_data):
    """Display the final results and feedback."""
    pass_mark = total_questions * 0.7  # 70% pass mark
    feedback = {}

    if total_score >= pass_mark:
        feedback['message'] = "Congratulations! You passed the quiz!"
        feedback['status'] = 'success'
    else:
        feedback['message'] = "Unfortunately, you did not pass the quiz. Please attempt the incorrect questions."
        feedback['status'] = 'error'

    results_data = []
    for question, user_answer, correct_answer, options in results:
        question_text = quiz_data[question]['mcq']
        status = "Correct" if user_answer == correct_answer else "Incorrect"
        results_data.append({
            "Question": question_text,
            "Your Answer": options[user_answer],
            "Correct Answer": options[correct_answer],
            "Status": status
        })
    
    results_df = pd.DataFrame(results_data)
    return feedback, results_df

def restart_quiz():
    """Reset the session state for a new quiz attempt."""
    return {
        'score': 0,
        'current_question': 0,
        'user_answers': {},
        'results': [],
        'attempts': {},
        'second_attempt': False
    }
