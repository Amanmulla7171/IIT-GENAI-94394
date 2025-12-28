import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as ps

load_dotenv()

llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

conversation = [
    {"role": "system", "content": "you are SQL query generator. with 10 years of experience in SQL."}
]

st.title("CSV to SQL Query Generator")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.dtypes)
    st.dataframe(df)

    user_input = st.text_input("Enter your question")

    if st.button("Generate SQL"):
        llm_input = f"""
        Table Name: df
        Table Schema: {df.dtypes}
        Question: {user_input}
        Instruction:
            Write a SQL query for the above question.
            Generate SQL query only in plain text format and nothing else.
            If you cannot generate the query, then output 'Error'.
        """

        result = llm.invoke(llm_input)
        sql_query = result.content.strip()

        st.write("Generated SQL Query")
        st.code(sql_query)

        if "Error" not in sql_query:
            query_result = ps.sqldf(sql_query, {"df": df})
            st.write("Query Result")
            st.dataframe(query_result)
        else:
            st.write(sql_query)
