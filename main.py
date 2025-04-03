import pytesseract
from langdetect import detect
from glob import glob
from os import path
from selenium_bot import upload

IMAGE_FOLDER = "Pictures"
OUTPUT_FILE = "recognized_text.txt"
pytesseract.pytesseract.tesseract_cmd = r"Tesseract\tesseract.exe"

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def get_tesseract_lang(lang_code):
    lang_map = {
        "en": "eng",
        "uk": "ukr"
    }
    return lang_map.get(lang_code, "eng")


def recognize_text_from_images():
    image_paths = glob(path.join(IMAGE_FOLDER, "*.*"))
    config = "--oem 3 --psm 3"
    if not image_paths:
        print("Немає зображень у папці.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for image_path in image_paths:
            raw_text = pytesseract.image_to_string(image_path, config=config, lang="eng+ukr+rus")
            detected_lang = detect_language(raw_text)
            tesseract_lang = get_tesseract_lang(detected_lang)
            final_text = pytesseract.image_to_string(image_path, config=config, lang=tesseract_lang)

            file.write(f"=== {path.basename(image_path)} ===\n")
            file.write(f"Мова: {tesseract_lang}\n")
            file.write(f"{final_text}\n\n")

    print(f"Розпізнаний текст збережено у {OUTPUT_FILE}")


if __name__ == "__main__":
    recognize_text_from_images()
    upload()