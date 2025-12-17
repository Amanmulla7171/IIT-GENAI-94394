import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import data

# Load environment
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config("Groq Chatbot", )

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- Login Page ----------------
def login_page():
    st.title("Login / Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if data.login_user(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Signup"):
            if data.register_user(username, password):
                st.success("Account created! Login now.")
            else:
                st.error("Username already exists")

# ---------------- Chat Page ----------------
def chat_page():
    st.title(f"Chatbot | User: {st.session_state.user}")

    with st.sidebar:
        if st.button("Clear Chat"):
            data.clear_messages(st.session_state.user)
            st.rerun()

        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    history_df = data.get_messages(st.session_state.user)

    messages_for_llm = []

    for _, row in history_df.iterrows():
        with st.chat_message(row["role"]):
            st.write(row["content"])
        messages_for_llm.append(
            {"role": row["role"], "content": row["content"]}
        )

    user_input = st.chat_input("Ask something...")

    if user_input:
        data.save_message(st.session_state.user, "user", user_input)

        with st.chat_message("user"):
            st.write(user_input)

        messages_for_llm.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=messages_for_llm,
                )
                reply = response.choices[0].message.content
                st.write(reply)

        data.save_message(st.session_state.user, "assistant", reply)
        st.rerun()

# ---------------- Routing ----------------
if st.session_state.user:
    chat_page()
else:
    login_page()
