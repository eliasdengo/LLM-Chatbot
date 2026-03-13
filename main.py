import os
from turtle import st
from dotenv import load_dotenv
import  google.generativeai  as genai
import streamlit as st
# Load environment variables from .env file
load_dotenv()

# configure streamlit page setting 
st.set_page_config(
    page_title="ChatBot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="expanded",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model=genai.GenerativeModel("gemini-1.5-flash")

# Function to Translate Role between gemini and streamlit 
def translate_role(role):
    if role == "user":
        return "user"
    elif role == "model":
        return "assistant"
    else:
        return "unknown"
# initial chat session in streamlit if not already exists
if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history=[])

# display chat bot title in the page 
st.title("ChatBot :robot:")

# display chat history in the page 
for message in st.session_state.messages.history:
    role = translate_role(message.role)
    with st.chat_message(role):
        st.markdown(message.parts[0].text)
# input form for user to send message to the chat bot
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submit_button = st.form_submit_button(label="Send")
    if submit_button and user_input:
        # get response from the chat bot
        response = st.session_state.messages.send_message(user_input)
