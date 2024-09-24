import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# Load environment variables from the .env file
load_dotenv()

# Load the JSON file with error handling
try:
    with open(r'C:\Users\Administrator\Documents\mcqgen\Response.json', 'r', encoding='utf-8') as file:
        content = file.read()
        print(content)  # Check the content of the file
        RESPONSE_JSON = json.loads(content)  # Load JSON here
except json.JSONDecodeError as e:
    st.error(f"JSON decode error: {str(e)}")
    RESPONSE_JSON = {}  # Set to an empty dict to avoid further errors
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    RESPONSE_JSON = {}  # Set to an empty dict to avoid further errors



# Create a title for the app
st.title("MCQs Creator Application with LangChain")

# Create a form using st.form
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file", type=["pdf", "txt"])
    
    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=1, max_value=20, value=5)
    subject = st.text_input("Subject")
    tone = st.selectbox("Tone", ["Formal", "Informal"])
    
    # Submit Button
    submitted = st.form_submit_button("Generate MCQs")
    
    if submitted:
        if uploaded_file is not None:
            # Read the file content
            if uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode("utf-8")
            else:
                # For PDF files, you'd typically use PyPDF2 or similar library
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            # Prepare the input for the LangChain
            try:
                response = generate_evaluate_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)  # Assuming you want to include this
                })
                
                # Extract the results from the response
                quiz_data = response.get("quiz", "").lstrip("### ").strip()
                review_data = response.get("review")
                
                # Display the quiz questions
                st.subheader("Generated MCQs:")
                st.json(quiz_data)  # Display the quiz in a JSON format
                
                # Display the review analysis
                st.subheader("Review Analysis:")
                st.write(review_data)  # Display review analysis
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

        else:
            st.warning("Please upload a file.")
