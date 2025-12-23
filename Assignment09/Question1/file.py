import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as ps

# Load environment variables
load_dotenv()

# Initialize LLM (same logic)
llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# System prompt (same)
conversation = [
    {"role": "system", "content": "you are SQL query generator. with 10 years of experience in SQL."}
]

# Streamlit UI

st.title("CSV to SQL Query Generator")




# Load CSV only once
path = st.text_input("Enter the path of CSV file")

st.write("Waiting for CSV path...")

if path and path.strip() != "":
    try:
        df = pd.read_csv(path, encoding="utf-8")
        st.success("CSV loaded successfully")
        st.write("### Table Schema")
        st.write(df.dtypes)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()


    # User question
    user_input = st.text_input("Ask a question on this table")

    # Generate SQL button
    if st.button("Generate SQL Query"):

        llm_input = f"""
        Table Name: df
        Table Schema: {df.dtypes}
        Question: {user_input}
        Instruction:
            Write a SQL query for the above question.
            Generate SQL query only in plain text format and nothing else.
            If you cannot generate the query, then output 'Error'.
        """

        # LLM call (same logic)
        result = llm.invoke(llm_input)
        sql_query = result.content.strip()

        st.write("### Generated SQL Query")
        st.code(sql_query)

        if "Error" in sql_query:
            st.error(sql_query)
        else:
            try:
                query_result = ps.sqldf(sql_query, {"df": df})
                st.write("### Query Result")
                st.dataframe(query_result)
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")

# Exit button
if st.button("Exit"):
    st.stop()
