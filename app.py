from openai import OpenAI
import streamlit as st
import logging
import time
from streamlit_chat import message


def sidebar():
    with st.sidebar:
        if st.button("Clear Conversation"):
            st.session_state['generated'] = []
            st.session_state['past'] = []
            st.session_state['messages'] = [
                {"role": "system", "content": "You are Paul, an AI Bible Buddy, who teaches the Bible to kids & youth"}
            ]
        st.caption("---")
        st.caption("""<div style="text-align: left;"><span style="font-family: Arial, Helvetica, sans-serif; font-size: 20px;">About</span></div>""",unsafe_allow_html=True)
        st.caption(
            """
            <div style="text-align: left;">
                <span style="font-family: Arial, Helvetica, sans-serif; font-size: 14px;">
                    AI Bible Buddy Chatbot is an engaging and interactive app designed for kids and youth to explore and learn about the Bible. 
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption("---")

        st.caption(
            """
            <div style="text-align: left;">
                <h3>How does AI Bible Buddy work?</h3>
                <p style="font-family: Arial, Helvetica, sans-serif; font-size: 14px;">
                    When you ask a question or request a Bible verse, AI Bible Buddy processes your input using advanced AI algorithms. AI Bible Buddy utilizes an advanced LLM model developed by OpenAI, designed with millions of parameters and highly trained on the Bible and related texts. It generates a thoughtful and accurate response, providing context and explanations to help you understand and connect with the Bible better.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("<br><br>&copy;2024 aibiblebuddy.online. All rights reserved." , unsafe_allow_html=True)

# Setting page title and header
st.set_page_config(page_title="My Bible Buddy: AI Assistant", page_icon="📖", layout="wide")
st.subheader("AI Bible Buddy 📖",divider='grey')

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI API key
sidebar()

try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
except KeyError:
    st.error("Please set the OpenAI API key in the secrets.toml file.")
    st.stop()

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are Paul, an AI Bible Buddy, who teaches the Bible to kids & youth"}
    ]

# Reset everything

def generate_response(prompt):
    """
    Generates a response from the OpenAI API.

    Args:
        prompt (str): The user's input prompt.

    Returns:
        str: The generated response from OpenAI.
    """
    try:
        st.session_state['messages'].append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state['messages']
        )
        
        if completion.choices and completion.choices[0].message and completion.choices[0].message.content:
            response = completion.choices[0].message.content
            st.session_state['messages'].append({"role": "assistant", "content": response})
            return response
        else:
            raise ValueError("No valid response content")
    
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        st.error("An error occurred while generating the response. Please try again.")
        return ""

# Container for chat history
response_container = st.container()

if user_input := st.chat_input("'I'm AI Bible Buddy. How can I assist you with your Bible learning today?'"):
    st.session_state['past'].append(user_input)
    #message(user_input, is_user=True)
    with st.spinner('Waiting for response...',):
        if output := generate_response(user_input):
            st.session_state['generated'].append(output)

       
if st.session_state['generated']:    
    for i in range(len(st.session_state['generated'])):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i), avatar_style="initials", seed="AI")




    
        




