from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os
import getpass


# Load environment variables from the .env file
load_dotenv(find_dotenv(), override=True)
if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Provide your Google API Key: ')

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Template for generating quiz
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template="""
    Text: {text}
    You are an expert MCQ maker. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to conform to the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs.
    ### RESPONSE_JSON
    {response_json}
    """
)

# Template for evaluating quiz
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template="""
    You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, \
    you need to evaluate the complexity of the question and give a complete analysis of the quiz. Use at max 50 words for complexity analysis. 
    If the quiz is not up to the cognitive and analytical abilities of the students, \
    update the quiz questions that need changes and change the tone to perfectly fit the students' abilities.
    Quiz_MCQs:
    {quiz}
    """
)

# Define chains
quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Define the SequentialChain
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)

def generate_and_evaluate_quiz(text, number, subject, tone, response_json):
    """
    Generate a quiz and evaluate it based on the given parameters.
    """
    result = generate_evaluate_chain({
        "text": text,
        "number": number,
        "subject": subject,
        "tone": tone,
        "response_json": response_json
    })
    return result
