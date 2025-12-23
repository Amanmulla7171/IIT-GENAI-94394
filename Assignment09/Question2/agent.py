from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@tool
def scraper():
    """
    Retrieves Sunbeam internship batch and program information.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    data = {
        "batches": [],
        "programs": []
    }

    try:
        driver.get("https://sunbeaminfo.in/internship")
        driver.implicitly_wait(5)

        table = driver.find_element(
            By.CSS_SELECTOR,
            "table.table.table-bordered.table-striped"
        )

        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 7:
                continue

            data["batches"].append({
                "sr": cols[0].text,
                "batch": cols[1].text,
                "duration": cols[2].text,
                "start": cols[3].text,
                "end": cols[4].text,
                "time": cols[5].text,
                "price": cols[6].text
            })

        driver.get("https://sunbeaminfo.in/internship")
        wait = WebDriverWait(driver, 10)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        plus_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
        plus_button.click()

        table = driver.find_element(By.ID, "collapseSix")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            data["programs"].append({
                "technology": cols[0].text,
                "aim": cols[1].text,
                "prerequisite": cols[2].text,
                "learning": cols[3].text,
                "location": cols[4].text
            })

    finally:
        driver.quit()

    return data


llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


agent = create_agent(
    model=llm,
    tools=[scraper],
    system_prompt=(
        "You are a web scraping assistant."
        "You retrieve Sunbeam internship and batch data using the scraper tool."
        "Answer user questions using the scraped data."
        "Maintain conversation context."
        "If a tool is used, respond with only the final answer."
    )
)


chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    chat_history.append({"role": "user", "content": user_input})

    result = agent.invoke({
        "messages": chat_history
    })

    ai_message = result["messages"][-1]
    chat_history.append(ai_message)

    print("AI:", ai_message.content)
