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
    {"role": "system", "content": "you are SQL query generator. with 10 years of experience in SQL. "}
]

path=input("Enter the path of csv file: ")
df=pd.read_csv(path)
print(df.dtypes)



while True:
    user_input = input("You: ")
    if user_input == "exit":
      break

    llm_input = f"""
        Table Name: df
        Table Schema: {df.dtypes}
        Question: {user_input}
        Instruction:
            Write a SQL query for the above question. 
            Generate SQL query only in plain text format and nothing else.
            If you cannot generate the query, then output 'Error'.
     """


    result=llm.invoke(llm_input)
    print(result.content)

    sql_query=result.content.strip()
    if "Error" in sql_query:
        print(sql_query)
        continue
    print("Generated SQL Query: ", sql_query)
    query_result = ps.sqldf(sql_query, {"df": df})
    print(query_result)
