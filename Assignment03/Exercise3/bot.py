import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import data 


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config("Groq Chatbot")

# Session state
if "user" not in st.session_state:
    st.session_state.user = None


#history page
def history_page():
    st.title("Chat History")


    if st.button("Back to Chat"):
        st.session_state.page = "chat"
        st.rerun()

    st.divider()

    chats = data.get_user_chats(st.session_state.user)

    if chats.empty:
        st.info("No previous chats found")
        return

    for idx, row in chats.iterrows():
        chat_id = row["chat_id"]

        col1, col2 = st.columns([3, 1])

        with col1:
            if st.button(f"Open Chat {idx+1}", key=f"open_{chat_id}",width="stretch"):
                st.session_state.chat_id = chat_id
                st.session_state.page = "chat"
                st.rerun()

        with col2:
            if st.button("Delete", key=f"delete_{chat_id}",width="stretch"):
                data.delete_chat(st.session_state.user, chat_id)
                st.success("Chat deleted")
                st.rerun()

#login page
def login_page():
    st.title("Login / Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)



    with col1:
        if st.button("Login",use_container_width=True):
            if data.login_user(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Signup",use_container_width=True):
            if data.register_user(username, password):
                st.success("Account created! Login now.")
            else:
                st.error("Username already exists")


#chat page
def chat_page():
    st.title(f"🤖 Chatbot |Hi {st.session_state.user}")

    # Initialize chat id
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = data.new_chat_id()

    # Sidebar
    with st.sidebar:
        if st.button("New Chat",width="stretch"):
            st.session_state.chat_id = data.new_chat_id()
            st.rerun()

        if st.button("History",width="stretch"):
            st.session_state.page = "history"
            st.rerun()

        st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        st.divider()

        if st.button("Logout",width="stretch"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

    #load chat history
    history = data.get_chat_messages(
        st.session_state.user,
        st.session_state.chat_id
    )

    messages_for_llm = []

    for _, row in history.iterrows():
        with st.chat_message(row["role"]):
            st.write(row["content"])
        messages_for_llm.append(
            {"role": row["role"], "content": row["content"]}
        )

 ## Chat input
    user_input = st.chat_input("Ask something...")

    if user_input:
        data.save_message(
            st.session_state.user,
            st.session_state.chat_id,
            "user",
            user_input
        )

        messages_for_llm.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_llm
                )
                reply = response.choices[0].message.content
                st.write(reply)

        data.save_message(
            st.session_state.user,
            st.session_state.chat_id,
            "assistant",
            reply
        )
        st.rerun()



# Main logic
if "page" not in st.session_state:
    st.session_state.page = "chat"

if st.session_state.user is None:
    login_page()
elif st.session_state.page == "history":
    history_page()
else:
    chat_page()

