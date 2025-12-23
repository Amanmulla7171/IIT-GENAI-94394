from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os

import command  # your watcher/command module

load_dotenv()

COMMAND_FILE = "commands.txt"


@tool
def youtube_search(query: str) -> str:
    """
    Use this tool to control the YouTube automation.

    Mapping:
      - If user wants to play something: PLAY_VIDEO <query...>
      - If user says close/stop/off:    CLOSE_VIDEO

    The background script (command.process_commands or watch_and_execute_commands)
    will read commands.txt and execute the Selenium automation.
    """
    text = query.strip().lower()

    if "close" in text or "stop" in text or "off" in text:
        cmd_line = "CLOSE_VIDEO"
    else:
        cmd_line = f"PLAY_VIDEO {query}"

    with open(COMMAND_FILE, "a", encoding="utf-8") as f:
        f.write(cmd_line + "\n")

    return f"Queued command: {cmd_line}"


# Initialize the language model
llm = init_chat_model(
    model="llama-3.2-3b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)


agent = create_agent(
    model=llm,
    tools=[youtube_search],
    system_prompt="""
You are a helpful assistant that controls a YouTube automation script via a tool.
When the user asks to play something, call youtube_search with their query.
When the user asks to stop/close the video, call youtube_search with text that includes 'close' or 'stop'.
Only talk to the user; the actual playing happens in the external script.
"""
)


if __name__ == "__main__":
    while True:
        user_input = input("ask anything:- ").strip()
        if user_input.lower() == "exit":
            break

        result = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        ai_message = result["messages"][-1]
        print("AI:", ai_message.content)
