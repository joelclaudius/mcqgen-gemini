from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks import get_openai_callback
import PyPDF2
from langchain import PromptTemplate, LLMChain
import os
import getpass
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import traceback
import json


# Load environment variables from the .env file
load_dotenv(find_dotenv(), override=True)
if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Provide your Google API Key: ')
# Access the environment variables


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
template = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to conform to the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs.
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)

# Updated initialization update
quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

template2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, \
you need to evaluate the complexity of the question and give a complete analysis of the quiz. Use at max 50 words for complexity analysis. 
If the quiz is not up to the cognitive and analytical abilities of the students, \
update the quiz questions that need changes and change the tone to perfectly fit the students' abilities.
Quiz_MCQs:
{quiz}
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Define the SequentialChain
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)
