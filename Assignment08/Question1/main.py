from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
from dotenv import load_dotenv
import os
import json
import requests
import ast
import operator
import pandas as pd

# Load environment variables
load_dotenv()



@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"
    

@tool
def get_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'    
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        data = response.json()

        

        return json.dumps(data)
    except:
        return "Error"


@tool
def read_file(filepath: str) -> str:
    """
    Reads a text file and returns its content.
    given the file path as input.
    :param filepath: str - path to the text file
    :returns: str - content of the file or error message

    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error: {str(e)}"
    


@wrap_model_call
def limit_context(request, handler):
    # Why: avoid mutating request in-place (LangChain requirement)
    request = request.override(
        messages=request.messages[-6:]
    )
    return handler(request)


@wrap_model_call
def normalize_response(request, handler):
    response = handler(request)

    if response.result and response.result[0].content:
        response.result[0].content = response.result[0].content.strip()

    return response





llm = init_chat_model(
    model="llama-3.2-3b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)



agent = create_agent(
    model=llm,
    tools=[calculator, get_weather, read_file],
    middleware=[limit_context, normalize_response],
    system_prompt="""
You are a helpful AI assistant.

IMPORTANT RULES:
1. Use tools only when required.
2. Never expose raw tool output.
3. Summarize results naturally.
4. Extract only useful data from JSON.
5. Never mention tools.
6. Keep answers short and clear.
"""
)   






while True:
    
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
           break

        response = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        

        print("AI:", response["messages"][-1].content)
        print()

    
