# Q&A Chatbot
from langchain.llms import OpenAI
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
from time import time
import pickle
import os

load_dotenv()  # take environment variables from .env.

root=os.getcwd()
file_name=os.getenv('RESPONCE_FILE_NAME') 

# function that write the responses 
def write_response(q,a):
    if file_name not in os.listdir(root):
        temp=dict()
        temp.update({time():[q,a]}) 
        pickle.dump(temp,open(os.path.join(root,file_name),'wb'))
    else:
        temp=pickle.load(open(os.path.join(root,file_name),'rb'))
        temp.update({time():[q,a]}) 
        pickle.dump(temp,open(os.path.join(root,file_name),'wb'))

## Function to load OpenAI model and get respones
def get_openai_response(question):
    llm=OpenAI(openai_api_key=os.getenv('LLM_API_KEY') ,model_name="text-davinci-003",temperature=0.5)
    response=llm(question)
    write_response(question,response)
    return response

# function for fetch history 
def fetch_history():
    temp=pickle.load(open(os.path.join(root,file_name),'rb'))
    if len(temp) > 20:
        for k in temp:
            del temp[k]
            if len(temp) == 20:
                break
    pickle.dump(temp,open(os.path.join(root,file_name),'wb'))
    return temp

##initialize our streamlit app
st.set_page_config(page_title="Q&A")
st.markdown("<h1 style='text-align: center; color: yellow;'>Chatbot Application Using Langchain</h1>", unsafe_allow_html=True)
st.markdown("***")

choice = st.sidebar.radio(
    label = "Choose the option" ,
    options = ("Question & Answer" , "History"))

if choice == "Question & Answer":
    prompt = st.chat_input("Say something")
    if prompt:
        st.markdown(f"### You : {prompt}")
        response=get_openai_response(prompt)
        st.markdown(" ")
        st.markdown(f"### Bot : {response}")

elif choice == "History":
    try :
        temp=fetch_history()
        if len(temp) > 0:
            for k in temp:
                q,a = temp[k]
                st.markdown(f"#### You : {q}")
                st.markdown(f"#### Bot : {a}")
    except FileNotFoundError:
         st.markdown("### There is no chat response has been made")
