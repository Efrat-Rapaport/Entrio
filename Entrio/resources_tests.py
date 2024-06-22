from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

import time
from config import resource_url,ebook_form_url,privacy_url


def test_page_load_in_5_seconds():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options,
                              desired_capabilities=capabilities)

    try:
        start_time = time.time()
        driver.get(resource_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        end_time = time.time()
        load_time = end_time - start_time
        print(f"Page load time: {load_time:.2f} seconds")

        assert load_time < 5, f"Page load time exceeds acceptable range: {load_time:.2f} seconds"

    finally:
        driver.quit()


def test_console_clean_from_errors_warnings():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options,
                              desired_capabilities=capabilities)

    try:
        driver.get(resource_url)
        logs = driver.get_log('browser')
        console_errors = [entry for entry in logs if entry['level'] == 'SEVERE']
        console_warnings = [entry for entry in logs if entry['level'] == 'WARNING']

        assert not console_errors, f"Console errors found: {console_errors}"
        assert not console_warnings, f"Console warnings found: {console_warnings}"
        print("No console errors or warnings found.")

    finally:
        driver.quit()


def test_privacy_policy_link_opens_in_new_tab_with_correct_url():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(ebook_form_url)
        time.sleep(10)
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe.hs-form-iframe')
        driver.switch_to.frame(iframe)
        privacy_policy_link = driver.find_element(By.XPATH, '//a[@href="https://www.entrio.io/privacy-policy" and text()="Privacy Policy"]')
        privacy_policy_link.click()
        driver.switch_to.window(driver.window_handles[1])
        current_url = driver.current_url
        assert current_url==privacy_url, f"Expected URL: {privacy_url}, but got: {current_url}"

    finally:
        driver.quit()
