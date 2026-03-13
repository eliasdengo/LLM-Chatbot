"""
ChatBot using Google's Gemini AI
Compatible with Python 3.9+
"""
import streamlit as st
import google.generativeai as genai
import os

# Page config must be first
st.set_page_config(
    page_title="Gemini ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Gemini ChatBot")

# Get API key from secrets (for Streamlit Cloud)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Fall back to environment variable (for local development)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    if not GOOGLE_API_KEY:
        st.error("""
        ⚠️ Google API Key not found!
        
        For Streamlit Cloud:
        1. Go to your app dashboard
        2. Click on 'Manage app' → 'Settings' → 'Secrets'
        3. Add: GOOGLE_API_KEY = "your-api-key"
        
        For local development:
        Create a .env file with: GOOGLE_API_KEY=your-api-key
        """)
        st.stop()

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Failed to initialize Gemini: {e}")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("What would you like to know?")

if prompt:
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
                st.error(f"Error: {e}")
