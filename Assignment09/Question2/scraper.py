from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://sunbeaminfo.in/internship")
    print("Page Title:", driver.title)

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

        info = {
            "sr": cols[0].text,
            "batch": cols[1].text,
            "batch duration": cols[2].text,
            "start date": cols[3].text,
            "end date": cols[4].text,
            "time": cols[5].text,
            "price": cols[6].text
        }

        print(info)

    driver.get("https://sunbeaminfo.in/internship")

    driver.implicitly_wait(5)
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

        info = {
            "technology": cols[0].text,
            "aim": cols[1].text,
            "prerequisite": cols[2].text,
            "learning": cols[3].text,
            "location": cols[4].text
        }

        print(info)

finally:
    driver.quit()
