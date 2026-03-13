import sys
import pkg_resources
import streamlit as st

st.set_page_config(page_title="Diagnostic", page_icon="🔧")

st.title("🔧 Diagnostic Tool")

st.subheader("System Info")
st.write(f"Python version: {sys.version}")
st.write(f"Python executable: {sys.executable}")
st.write(f"Python path: {sys.path}")

st.subheader("Installed Packages")
installed_packages = [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
installed_packages.sort()

for package in installed_packages:
    st.write(f"- {package}")

st.subheader("Check Google Generative AI")
try:
    import google.generativeai as genai
    st.success("✅ google.generativeai is installed!")
    st.write(f"Location: {genai.__file__}")
except ImportError as e:
    st.error(f"❌ Import failed: {e}")
    
st.subheader("Check Streamlit Version")
st.write(f"Streamlit version: {st.__version__}")
