import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Test", page_icon="🇩🇪")

# Check if the secret exists
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("SECRET MISSING: Your GOOGLE_API_KEY is not in the Streamlit Secrets box!")
    st.stop()

# Configure
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Use the most basic model name possible
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Schreib etwas..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simple generation
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"ENGINE ERROR: {e}")
