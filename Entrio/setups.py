from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import contact_url


def submit_contact_form(driver,first_name,last_name,email):
    driver.get(contact_url)
    wait = WebDriverWait(driver, 10)

    time.sleep(10)
    iframe = driver.find_element(By.CSS_SELECTOR, 'iframe.hs-form-iframe')
    driver.switch_to.frame(iframe)

    first_name_input = wait.until(EC.presence_of_element_located((By.NAME, "firstname")))
    first_name_input.send_keys(first_name)

    last_name_input = driver.find_elements(By.NAME, "lastname")[0]
    last_name_input.send_keys(last_name)

    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(email)

    submit_button = driver.find_element(By.CSS_SELECTOR, 'input.hs-button.primary.large[type="submit"]')
    submit_button.click()