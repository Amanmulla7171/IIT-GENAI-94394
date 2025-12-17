import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing")

local_api_key = os.getenv("local_api_key")
if not local_api_key:
    raise ValueError("Local API key is missing")

st.set_page_config(
    page_title="Chatbot",
    page_icon="$",
    layout="wide"
)

# import for exit button
import streamlit.components.v1 as components

# session state
if "user" not in st.session_state:
    st.session_state.user = "Select Model"

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:

    if st.button("New chat", use_container_width=True):
        st.session_state.user = "Select Model"
        st.session_state.messages = []
        st.rerun()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages.clear()
        st.rerun()

        
    st.markdown("<br>", unsafe_allow_html=True)
    # 🔹 MODEL SELECTION (REPLACED BUTTONS)
    selected_model = st.selectbox(
        "Select Model",
        ["Local Models", "Groq Models"],
        index=None
    )

    if selected_model == "Local Models" and st.session_state.user != "local_user":
        st.session_state.user = "local_user"
        st.session_state.messages = []
        st.rerun()

    if selected_model == "Groq Models" and st.session_state.user != "groq_user":
        st.session_state.user = "groq_user"
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br>" * 14, unsafe_allow_html=True)


    

    if st.button("Exit"):
        components.html(
            """
            <script>
                window.open('', '_self').close();
            </script>
            """,
            height=0,
        )
        st.stop()

st.title(f"CHATBOT : {st.session_state.user}")


# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# user input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Prepare and send request to appropriate API
    if st.session_state.user == "local_user":
        url = "http://10.83.202.71:1234/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {local_api_key}"
        }
        payload = {
            "model": "llama-3.2-3b-instruct",
            "messages": st.session_state.messages
        }

        res = requests.post(url, headers=headers, json=payload)
        response = res.json()["choices"][0]["message"]["content"]

    elif st.session_state.user == "groq_user":
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": st.session_state.messages
        }

        res = requests.post(url, headers=headers, json=payload)
        response = res.json()["choices"][0]["message"]["content"]

    else:
        response = "Please select a model first."

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)
