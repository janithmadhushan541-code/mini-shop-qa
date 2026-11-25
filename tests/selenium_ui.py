
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

# Create screenshot folder
Path("evidence").mkdir(exist_ok=True)

# Browser configuration
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)


def click_button(locator):
    element = wait.until(
        EC.element_to_be_clickable(locator)
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', "
        "behavior: 'instant'});",
        element
    )

    time.sleep(1)

    # Wait until the button is not covered by another element
    wait.until(lambda d: d.execute_script("""
        const el = arguments[0];
        const r = el.getBoundingClientRect();
        const target = document.elementFromPoint(
            r.left + r.width / 2,
            r.top + r.height / 2
        );
        return target === el || el.contains(target);
    """, element))

    element.click()


try:
    print("=" * 55)
    print("MINI SHOP - SELENIUM UI AUTOMATION TESTING")
    print("=" * 55)

    # TEST 01 - Open application
    driver.get("http://localhost:5173")

    add_locator = (
        By.XPATH,
        "//button[normalize-space()='Add']"
    )

    wait.until(
        EC.visibility_of_element_located(add_locator)
    )

    print("[PASS] TC-01: Application loaded successfully")

    driver.save_screenshot("evidence/catalog.png")

    # TEST 02 - Add product to cart
    click_button(add_locator)

    # Open cart if it is not already open
    if not driver.find_elements(By.TAG_NAME, "aside"):
        click_button((
            By.XPATH,
            "//header//button[contains(., 'Cart')]"
        ))

    wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "aside article"
        ))
    )

    wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//aside//button[normalize-space()='Checkout']"
        ))
    )

    print("[PASS] TC-02: Product added to shopping cart")

    driver.save_screenshot("evidence/cart.png")

    # TEST 03 - Clear shopping cart
    click_button((
        By.XPATH,
        "//aside//button[normalize-space()='Clear']"
    ))

    wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//h3[normalize-space()='Your cart is empty']"
        ))
    )

    print("[PASS] TC-03: Shopping cart cleared successfully")

    driver.save_screenshot("evidence/empty_cart.png")

    # Final test summary
    print("=" * 55)
    print("TEST EXECUTION SUMMARY")
    print("=" * 55)
    print("Total Test Cases : 3")
    print("Passed           : 3")
    print("Failed           : 0")
    print("Success Rate     : 100%")
    print("Status           : ALL TESTS PASSED")
    print("=" * 55)
    print("Screenshots saved in evidence folder")

    time.sleep(3)

except Exception as error:
    print("[FAIL] Selenium test execution failed")
    print(type(error).__name__)
    print(str(error))

    driver.save_screenshot("evidence/error.png")

    raise

finally:
    driver.quit()
