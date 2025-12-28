import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("Ask Employees Database")

host = "localhost"
user = "root"
password = "your_pass"
database = "test_db"

schema = """
employees(
id INT,
name VARCHAR,
department VARCHAR,
salary INT,
joining_date DATE
)
"""

question = st.text_input("Ask a question")

if st.button("Submit"):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    prompt = f"""
    Database Schema:
    {schema}

    Question:
    {question}

    Instruction:
    Generate only a SELECT SQL query.
    """

    sql_query = llm.invoke(prompt).content.strip()
    st.code(sql_query)

    cursor.execute(sql_query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    st.dataframe(rows, columns=columns)

    explain_prompt = f"Explain this SQL query in simple English:\n{sql_query}"
    explanation = llm.invoke(explain_prompt).content
    st.write(explanation)

    cursor.close()
    conn.close()
