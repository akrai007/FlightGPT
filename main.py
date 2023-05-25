#openai_api_key=''
#SERPAPI_API_KEY='...'

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import streamlit as st
from langchain import PromptTemplate
import json


st.set_page_config(page_title="Flight Search AI Agent", page_icon=":robot:")
st.header("Your friendly Flight GPT")

col1, col2= st.columns(2)

st.markdown("## Enter Your Flight Query")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

def get_serpapi_key():
    input_text = st.text_input(label="Serp API Key ",  placeholder="Ex: 2twmA8tfCb8un4...", key="serp_api_key_input")
    return input_text

serp_api_key = get_serpapi_key()


def get_text():
    input_text = st.text_area(label="Flight Query", label_visibility='collapsed', placeholder="Your query...", key="query_input")
    return input_text

query_input = get_text()

if len(query_input.split(" ")) > 700:
    st.write("Please enter a shorter query. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.query_input = """what is the cheapest flight between new york and Chicago for 10th June 2023, departure time 8 AM EST" 
    "share a flight booking link for the cheapest flight?"""

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Query result:")

if query_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    toolkit = load_tools(["serpapi"], llm=llm, serpapi_api_key=serp_api_key)

    agent = initialize_agent(toolkit, llm, agent="zero-shot-react-description", verbose=True, return_intermediate_steps=True)

    response = agent({query_input})

    st.write(response["output"])