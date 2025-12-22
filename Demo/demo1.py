from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the Groq_api_key environment variable.")
chat =  ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)

user_input=input("Enter your question: ")
response = chat.stream([HumanMessage(content=user_input)])
for chunk in response:
    print(chunk.content, end="")