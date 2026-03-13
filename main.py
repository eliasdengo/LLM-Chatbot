import os
import streamlit as st
import google.generativeai as genai

# Try to load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available

# Configure streamlit page setting
st.set_page_config(
    page_title="ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Get API key from Streamlit secrets or environment variables
# For Streamlit Cloud: Set up GOOGLE_API_KEY in Secrets
# For local: Use .env file or set environment variable
GOOGLE_API_KEY = None

# Try to get from Streamlit secrets first (for Streamlit Cloud)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Fall back to environment variable (for local development)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API key is available
if not GOOGLE_API_KEY:
    st.error("""
        ⚠️ Google API Key not found! 
        
        If running locally:
        - Create a .env file with GOOGLE_API_KEY=your_key_here
        
        If on Streamlit Cloud:
        - Add GOOGLE_API_KEY to your app secrets
    """)
    st.stop()

# Configure Google AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Failed to configure Google AI: {str(e)}")
    st.stop()

# Function to translate role for display
def translate_role(role):
    if role == "user":
        return "user"
    elif role == "model":
        return "assistant"
    return "unknown"

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display title
st.title("🤖 ChatBot")

# Display chat history
for message in st.session_state.messages:
    role = translate_role(message.role)
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    try:
        # Get response from chatbot
        with st.spinner("Thinking..."):
            response = st.session_state.chat_session.send_message(user_input)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # Update message history
        st.session_state.messages = st.session_state.chat_session.history
        st.rerun()
        
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
