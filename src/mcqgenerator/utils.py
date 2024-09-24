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
        raise Exception("Unsupported file format. Please upload a .pdf or .txt file.")


def get_table_data(quiz_str):
    try:
        quiz_str_cleaned = quiz_str.replace('### RESPONSE_JSON', '').strip()
        quiz_dict = json.loads(quiz_str_cleaned)
        quiz_table_data = []

        for question_num, question_data in quiz_dict.items():
            mcq = question_data.get("mcq", "N/A")
            options = "\n".join(
                [f"({option}) {option_value}" for option, option_value in question_data.get("options", {}).items()]
            )
            correct = question_data.get("correct", "N/A")

            quiz_table_data.append({"Question": mcq, "Options": options, "Correct Answer": correct})

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


