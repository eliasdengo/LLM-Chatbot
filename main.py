"""
Simple ChatBot using Google's Gemini AI
"""
import streamlit as st

# Page config must be first
st.set_page_config(
    page_title="Simple ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Try to import google.generativeai
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    st.error("""
    ❌ Google Generative AI package not found!
    
    This app requires 'google-generativeai' to be installed.
    
    If you're the app owner:
    1. Make sure requirements.txt exists with: google-generativeai
    2. Check deployment logs for installation errors
    3. Try specifying an older Python version in runtime.txt
    """)
    st.stop()

import os

st.title("🤖 Simple ChatBot")

# Get API key
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ API key found!")
except:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("❌ No API key found. Please add it to secrets.")
        st.stop()

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.success("✅ Gemini initialized!")
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini: {e}")
    st.stop()

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append(
                {"role": "assistant", "content": response.text}
            )
