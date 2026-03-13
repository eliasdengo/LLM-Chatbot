import os
import streamlit as st
import google.generativeai as genai

# configure streamlit page setting 
st.set_page_config(
    page_title="ChatBot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Get API key - works both locally and on Streamlit Cloud
# For local development, you can still use .env or set environment variable
# For Streamlit Cloud, set this in Secrets (see instructions below)
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

if not GOOGLE_API_KEY:
    st.error("Please set your GOOGLE_API_KEY in environment variables or Streamlit secrets")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to Translate Role between gemini and streamlit 
def translate_role(role):
    if role == "user":
        return "user"
    elif role == "model":
        return "assistant"
    else:
        return "unknown"

# initial chat session in streamlit if not already exists
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat bot title in the page 
st.title("ChatBot :robot:")

# display chat history in the page 
for message in st.session_state.messages:
    role = translate_role(message.role)
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# input for user to send message to the chat bot
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to display
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # get response from the chat bot
    response = st.session_state.chat_session.send_message(user_input)
    
    # Add assistant response to display
    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    # Update messages in session state
    st.session_state.messages = st.session_state.chat_session.history
    st.rerun()
