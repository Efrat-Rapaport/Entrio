from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
import time

from Entrio.setups import submit_contact_form
from config import roi_url, valid_email, valid_last_name, valid_first_name, invalid_email, annual_cost_avoidance_and_productivity_gains,estimated_savings_from_consolidations,annual_technology_spend,total_number_of_vendors,number_of_new_vendors_on_average_per_year,number_of_employees


def test_succeed_submit_contact_form_with_valid_and_required_fields():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver, 10)
    try:
        submit_contact_form(driver, valid_first_name, valid_last_name, valid_email)
        try:
            submitted_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'submitted-message'))
            )
            get_submitted_message=True

        except Exception as e:
            get_submitted_message = False

        assert get_submitted_message, f"failed submit contact form"

    finally:
        driver.quit()


def test_failed_submit_contact_form_without_required_fields():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        submit_contact_form(driver, valid_first_name, valid_last_name, "")

        try:
            submitted_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'submitted-message'))
            )
            get_submitted_message=True

        except Exception as e:
            get_submitted_message = False

        assert not get_submitted_message, f"success submit contact form without required field"

    finally:
        driver.quit()


def test_failed_submit_contact_form_with_invalid_fields():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        submit_contact_form(driver, valid_first_name, valid_last_name, invalid_email)
        try:
            submitted_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'submitted-message'))
            )
            get_submitted_message = True

        except Exception as e:
            get_submitted_message = False

        assert not get_submitted_message, f"success submit contact form with invalid field"
    finally:
        driver.quit()


def test_roi_calculator_work():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    try:
        driver.get(roi_url)
        time.sleep(5)
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src='https://app.entrio.io/roi/calculator']")
        driver.switch_to.frame(iframe)

        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.form-group")

        input_number_of_employees = div_elements[0].find_element(By.CSS_SELECTOR, "input.roi-slider-input")
        input_number_of_employees.send_keys(Keys.CONTROL + "a")
        input_number_of_employees.send_keys(Keys.BACKSPACE)
        input_number_of_employees.send_keys(number_of_employees)

        label_type_of_operation=div_elements[1].find_element(By.CSS_SELECTOR, 'label[for="local"]')
        label_type_of_operation.click()

        input_annual_technology_spend = div_elements[2].find_element(By.CSS_SELECTOR, "input.roi-slider-input")
        input_annual_technology_spend.send_keys(Keys.CONTROL + "a")
        input_annual_technology_spend.send_keys(Keys.BACKSPACE)
        input_annual_technology_spend.send_keys(annual_technology_spend)

        input_total_number_of_vendors = div_elements[3].find_element(By.CSS_SELECTOR, "input.roi-slider-input")
        input_total_number_of_vendors.send_keys(Keys.CONTROL + "a")
        input_total_number_of_vendors.send_keys(Keys.BACKSPACE)
        input_total_number_of_vendors.send_keys(total_number_of_vendors)

        input_number_of_new_vendors_on_average_per_year = div_elements[4].find_element(By.CSS_SELECTOR, "input.roi-slider-input")
        input_number_of_new_vendors_on_average_per_year.send_keys(Keys.CONTROL + "a")
        input_number_of_new_vendors_on_average_per_year.send_keys(Keys.BACKSPACE)
        input_number_of_new_vendors_on_average_per_year.send_keys(number_of_new_vendors_on_average_per_year)

        div_results = driver.find_elements(By.CSS_SELECTOR, "div.total-value")

        estimated_savings_from_consolidations_value=div_results[0].text
        estimated_savings_from_consolidations_value_str = estimated_savings_from_consolidations_value.replace('$', '').replace(',', '')
        estimated_savings_from_consolidations_value_int_from_roi = int(estimated_savings_from_consolidations_value_str)

        annual_cost_avoidance_and_productivity_gains_value=div_results[1].text
        annual_cost_avoidance_and_productivity_gains_str = annual_cost_avoidance_and_productivity_gains_value.replace('$', '').replace(',', '')
        annual_cost_avoidance_and_productivity_gains_int_from_roi = int(annual_cost_avoidance_and_productivity_gains_str)

        assert estimated_savings_from_consolidations_value_int_from_roi == estimated_savings_from_consolidations, f"ROI calculator is not functioning correctly. Expected result was not obtained."
        assert annual_cost_avoidance_and_productivity_gains_int_from_roi == annual_cost_avoidance_and_productivity_gains, f"ROI calculator is not functioning correctly. Expected result was not obtained."

    finally:
        driver.quit()

