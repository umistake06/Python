from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://books.toscrape.com/")

    books_data = []

    for page_num in range(5):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_pod")))
        book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for book in book_elements:
            try:
                title_elem = book.find_element(By.CSS_SELECTOR, "h3 a")
                title = title_elem.get_attribute("title").strip()

                price_elem = book.find_element(By.CSS_SELECTOR, "p.price_color")
                price = price_elem.text.strip()

                availability_elem = book.find_element(By.CSS_SELECTOR, "p.instock.availability")
                availability = availability_elem.text.strip()

                books_data.append({
                    "title": title,
                    "price": price,
                    "availability": availability
                })
            except Exception:
                continue

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
            next_url = next_btn.get_attribute("href")
            driver.get(next_url)
            time.sleep(1)
        except:
            break

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=2)

    target_title = "A Light in the Attic"
    found = False

    driver.get("https://books.toscrape.com/")

    for page_num in range(5):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_pod")))
        book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for book in book_elements:
            title_elem = book.find_element(By.CSS_SELECTOR, "h3 a")
            title = title_elem.get_attribute("title").strip()

            if title == target_title:
                link = title_elem.get_attribute("href")

                if link.startswith("../"):
                    link = link[3:]

                full_url = "https://books.toscrape.com/" + link
                driver.get(full_url)

                found = True
                break

        if found:
            break

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
            driver.get(next_btn.get_attribute("href"))
            time.sleep(1)
        except:
            break

    if found:
        driver.save_screenshot("book_screenshot.png")

finally:
    driver.quit()
