from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from contextlib import contextmanager
import os

@contextmanager
def getdriver():
    driver = None

    try:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.page_load_strategy = "eager"
        # options.add_argument("--headless")

        if os.getenv("USE_REMOTE_SELENIUM") == "true":
            driver = webdriver.Remote(
                command_executor=os.getenv("SELENIUM_REMOTE_URL"),
                options=options
            )
        else:
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        yield driver
    except Exception as e:
        print(f"Driver initialization failed: {str(e)}")
        raise
    finally:
        if driver:
            driver.quit()
            print("Driver terminated successfully")
