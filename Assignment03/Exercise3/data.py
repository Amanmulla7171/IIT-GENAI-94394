import pandas as pd
from pandasql import sqldf
import os
import uuid

USERS_FILE = "users.csv"
MESSAGES_FILE = "messages.csv"


#initialize files
def init_files():
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        pd.DataFrame(
            columns=["username", "password"]
        ).to_csv(USERS_FILE, index=False)

    if not os.path.exists(MESSAGES_FILE) or os.stat(MESSAGES_FILE).st_size == 0:
        pd.DataFrame(
            columns=["username", "chat_id", "role", "content"]
        ).to_csv(MESSAGES_FILE, index=False)


init_files()


#load users and messages
def load_users():
    df = pd.read_csv(USERS_FILE)
    df.columns = df.columns.str.lower()
    return df


def load_messages():
    df = pd.read_csv(MESSAGES_FILE)
    df.columns = df.columns.str.lower()
    return df


#user registration and login
def register_user(username, password):
    users = load_users()
    if username in users["username"].values:
        return False
    users.loc[len(users)] = [username, password]
    users.to_csv(USERS_FILE, index=False)
    return True


def login_user(username, password):
    users = load_users()
    return not users[
        (users.username == username) &
        (users.password == password)
    ].empty


#chat management
def new_chat_id():
    return str(uuid.uuid4())


def save_message(username, chat_id, role, content):
    df = load_messages()
    df.loc[len(df)] = [username, chat_id, role, content]
    df.to_csv(MESSAGES_FILE, index=False)


def get_chat_messages(username, chat_id):
    df = load_messages()
    query = f"""
    SELECT role, content FROM df
    WHERE username = '{username}'
    AND chat_id = '{chat_id}'
    """
    return sqldf(query, {"df": df})


def get_user_chats(username):
    df = load_messages()
    query = f"""
    SELECT DISTINCT chat_id FROM df
    WHERE username = '{username}'
    """
    return sqldf(query, {"df": df})
def get_messages(username):
    df = load_messages()
    query = f"""
    SELECT role, content FROM df
    WHERE username = '{username}'
    """
    return sqldf(query, {"df": df})



def delete_chat(username, chat_id):
    df = load_messages()

    query = f"""
    SELECT * FROM df
    WHERE NOT (username = '{username}' AND chat_id = '{chat_id}')
    """

    updated_df = sqldf(query, {"df": df})
    updated_df.to_csv(MESSAGES_FILE, index=False)

