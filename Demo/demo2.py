from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import os


llm_url = "http://127.0.0.1:1234/v1"
llm = ChatOpenAI(
    base_url=llm_url,
    model="llama-3.2-3b-instruct:2",
    api_key="dummy-key"
 )

user_input=input("ask anything: ")
#response = llm.stream([HumanMessage(content=user_input)])
#for chunk in response:
#    print(chunk.content, end="")

result = llm.invoke(user_input)
print("AI: ", result.content)