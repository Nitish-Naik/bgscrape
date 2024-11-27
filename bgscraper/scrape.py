from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json  


driver = webdriver.Edge()


driver.maximize_window()


all_verses_info = []


url = 'https://vedabase.io/en/library/bg/16/1-3/'
driver.get(url)


time.sleep(3)

try:
    for i in range(1, 20):  
        
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'r-title'))
        ).text
        
        
        print(f"Current Title: {title}")

        
        parts = title.split('.')
        if len(parts) == 3:  
            chapter = parts[1].strip()  
            verse_number = parts[2].strip()  
        elif len(parts) == 2 and '-' in parts[1]:  
            chapter = parts[1].split('-')[0].strip()  
            verse_range = parts[1].strip()  
        else:
            print(f"Unexpected title format: {title}")
            break  

        
        time.sleep(3)  
        verse_text_english = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'r-verse-text'))
        ).text

        
        time.sleep(3)  
        verse_text_devnagari = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'r-devanagari'))
        ).text

        
        time.sleep(3)  
        translation_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'r-translation'))
        ).text

        
        time.sleep(3)  
        synonyms_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'r-synonyms'))
        ).text  

        
        synonyms_pairs = [pair.strip() for pair in synonyms_text.split(';') if pair.strip()]

        
        verse_info = {
            "chapter": chapter,
            "verse": verse_number if 'verse_range' not in locals() else verse_range,  
            "verse_text_devnagari": verse_text_devnagari,
            "verse_text_english": verse_text_english,
            "Translation": translation_text,
            "Synonyms": synonyms_pairs
        }

        
        all_verses_info.append(verse_info)

        
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'pager-next'))
            )
            time.sleep(1)  
            next_button.click()
            time.sleep(3)  
        except Exception as e:
            print(f"No more verses found: {e}")
            break  

except Exception as e:
    print(f"Error during extraction: {e}")


try:
    with open("Chapter-16.txt", "w+", encoding="utf-8") as file:
        for verse in all_verses_info:
            file.write(json.dumps(verse, ensure_ascii=False) + "\n")  
except Exception as e:
    print(f"Error writing to file: {e}")


print("All Verses Information:", all_verses_info)


driver.quit()
