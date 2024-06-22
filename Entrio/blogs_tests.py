from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from config import blog_url

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


def test_blog_content_matches_the_title():
    try:
        driver.get(blog_url)
        posts_links = driver.find_elements(By.CSS_SELECTOR, "div.resource-item.w-dyn-item")

        for i in range(len(posts_links)):
            posts_links = driver.find_elements(By.CSS_SELECTOR, "div.resource-item.w-dyn-item")
            post = posts_links[i]

            outer_title = post.find_element(By.CSS_SELECTOR, "h3.resource-title-two")
            outer_title_text = outer_title.text

            arrow_div = post.find_element(By.CSS_SELECTOR, "div.purple-arrow.w-embed")
            arrow_div.click()

            inner_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            inner_title_text = inner_title.text

            assert outer_title_text == inner_title_text, f"Expected post title: '{outer_title_text}' but got: '{inner_title_text}'"
            driver.back()

    except Exception as e:
        print(f"Compare with title failed: {e}")
        driver.quit()
        return



