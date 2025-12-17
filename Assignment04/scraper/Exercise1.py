from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start the selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless=new")  
driver = webdriver.Chrome(options=chrome_options)

# load desired page
driver.get("https://sunbeaminfo.in/internship")
print("Page Title:", driver.title)

# define wait strategy
driver.implicitly_wait(10)

# 1. locate the collapse toggle button
toggle_button = driver.find_element(
    By.CSS_SELECTOR,
    "div.panel.panel-default.wow.fadeInUp a[data-toggle='collapse'][href='#collapseSix']"
)

toggle_button.click()

#wait 10 seconds 


# 3. now the table is visible — find it
element = driver.find_element(
    By.CSS_SELECTOR,
    "div.panel.panel-default.wow.fadeInUp"
)

table = element.find_element(By.ID, "collapseSix")  # expanded panel

tbody = table.find_element(By.TAG_NAME, "tbody")
rows = tbody.find_elements(By.TAG_NAME, "tr")

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    # skip header or empty rows
    if len(cols) < 5:
        continue

    info = {
        "technology": cols[0].text,
        "aim": cols[1].text,
        "prerequisite": cols[2].text,
        "learning": cols[3].text,
        "location": cols[4].text
    }
    print(info)

driver.quit()
