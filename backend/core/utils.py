from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def web_driver_wait_visibility_of_element_by_xpath(driver, xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
    except NoSuchElementException:
        return False
