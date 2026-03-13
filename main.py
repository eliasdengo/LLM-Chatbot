"""
Simple ChatBot using Google's Gemini AI
"""

import sys
import subprocess

# Try to install missing packages automatically (for debugging)
try:
    import streamlit as st
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

try:
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

import os

# Configure page
st.set_page_config(
    page_title="ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 ChatBot")

# Get API key from secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("""
    ⚠️ Google API Key not found!
    
    Please add your API key in Streamlit Cloud Secrets:
    1. Go to your app dashboard
    2. Click on 'Manage app' → 'Settings' → 'Secrets'
    3. Add:
    
    GOOGLE_API_KEY = "your-actual-api-key-here"
    """)
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Failed to initialize Gemini: {str(e)}")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
