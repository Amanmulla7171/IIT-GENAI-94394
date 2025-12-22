# youtube_automation.py

import os
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException

# configurations

CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")
CHROME_BINARY_PATH = os.environ.get("CHROME_BINARY_PATH", "/usr/bin/google-chrome")
DISPLAY = os.environ.get("DISPLAY", "192.168.146.168:0")

os.environ["DISPLAY"] = DISPLAY

YOUTUBE_HOME = "https://www.youtube.com"


# driver setup

def create_driver() -> webdriver.Chrome:
    chrome_options = Options()
    # On Windows, usually no need to set binary_location if Chrome is installed normally.

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=C:/tmp/chrome-profile")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("--mute-audio")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
#youtube automation functions



def search_and_open_first_video(driver: webdriver.Chrome, query: str) -> None:
    """
    Open YouTube, search by query, and open the first video result.
    Uses JS click to avoid click interception.
    """
    print(f"[YouTube] Searching for: {query!r}")
    driver.get(YOUTUBE_HOME)

    wait = WebDriverWait(driver, 20)

    # Search box
    search_box = wait.until(
        EC.element_to_be_clickable((By.NAME, "search_query"))
    )
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    # First video thumbnail
    first_video = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ytd-video-renderer a#thumbnail")
        )
    )

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_video)
    time.sleep(1)

    # Try normal click, fallback to JS click if intercepted
    try:
        first_video.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", first_video)

    print("[YouTube] Opened first video result.")



def force_play_video(driver: webdriver.Chrome) -> None:
    """
    Wait for main video element and call play() via JS.
    """
    wait = WebDriverWait(driver, 20)
    video = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "video.html5-main-video")
        )
    )
    driver.execute_script("arguments[0].play();", video)
    print("[YouTube] Video playback started (JS play).")




def try_skip_ad(driver: webdriver.Chrome) -> None:
    """
    Try to click any visible 'Skip Ad' button, if present.
    Safe to call repeatedly in a loop.
    """
    selectors = [
        "button.ytp-ad-skip-button",
        "button.ytp-ad-skip-button-modern",
        ".ytp-ad-skip-button.ytp-button",
        ".ytp-ad-skip-button-container",
        ".ytp-ad-skip-button-slot",
    ]  # multiple known selectors for skip button[web:87][web:148][web:151]

    for sel in selectors:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
        except Exception:
            continue

        try:
            if btn.is_displayed() and btn.is_enabled():
                # Use JS click to avoid overlay issues
                driver.execute_script("arguments[0].click();", btn)
                print(f"[YouTube] Skipped ad using selector: {sel}")
                return
        except StaleElementReferenceException:
            # DOM changed between find and click; ignore and move on
            continue
        except Exception:
            continue



def close_driver(driver: Optional[webdriver.Chrome]) -> None:
    """
    Safely close the browser.
    """
    if driver is not None:
        print("[YouTube] Closing browser...")
        driver.quit()
