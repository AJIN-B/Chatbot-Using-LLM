# Q&A Chatbot
from langchain.llms import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

print(os.getenv('LLM_API_KEY'))

def get_openai_response(question):
    llm=OpenAI(openai_api_key=os.getenv('LLM_API_KEY') ,model_name="text-davinci-003",temperature=0.5)
    response=llm(question)
    return response

#input=st.text_input("Input: ",key="input")
response=get_openai_response('can u help me to write a love poem')
print(response)





