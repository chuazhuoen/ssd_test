# test_app.py
import pytest
from app import app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# === Unit/Integration tests with Flask test client ===

def test_home_get():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    assert b'Enter Something' in res.data

def test_post_valid_input():
    client = app.test_client()
    res = client.post('/', data={'user_input': 'Hello'})
    assert res.status_code == 302  # Redirect to /new

def test_post_malicious_input():
    client = app.test_client()
    res = client.post('/', data={'user_input': '<script>alert(1)</script>'}, follow_redirects=True)
    assert b'Malicious input detected' in res.data

# === Selenium-based UI test ===

@pytest.mark.selenium
def test_selenium_input_flow():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("http://localhost:5000")
    input_field = driver.find_element(By.NAME, "user_input")
    input_field.send_keys("Hello World")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    assert "You entered:" in driver.page_source
    assert "Hello World" in driver.page_source

    driver.quit()
