from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="openai/gpt-oss-120b",   
    model_provider="openai",         
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.getenv("GROQ_API_KEY")
)

conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    user_msg = {"role": "user", "content": user_input}
    conversation.append(user_msg)

    slider = 2
    
    llm_output = llm.invoke([conversation[0]] + conversation[-slider:])
    print("AI:", llm_output.content)

    llm_msg = {"role": "assistant", "content": llm_output.content}
    conversation.append(llm_msg)