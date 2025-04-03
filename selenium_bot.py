from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from glob import glob
from os import path
from time import sleep

ROOT_FOLDER = r"Pictures"
OUTPUT_FILE = "dropmefiles_links.txt"


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def upload():
    driver = get_driver()
    driver.get("https://dropmefiles.com.ua/ua/")

    upload_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )

    files_to_upload = glob(path.join(ROOT_FOLDER, "*.*"))

    if not files_to_upload:
        print("Немає файлів для завантаження.")
        driver.quit()
        return

    upload_input.send_keys("\n".join(map(path.abspath, files_to_upload)))

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='dzen' and @value='1']"))
    ).click()

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "uploadBtn"))
    ).click()

    main_link = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputText"))
    ).get_attribute("value")

    delete_link = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "pass"))
    ).get_attribute("value")

    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
        file.write(f"Посилання на файли: {main_link}\n")
        file.write(f"Посилання для видалення: {delete_link}\n\n")

    print(f"Збережено: {OUTPUT_FILE}")

    sleep(5)
    driver.quit()


if __name__ == "__main__":
    upload()
