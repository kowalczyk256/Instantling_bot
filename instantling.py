import os
import sqlite3
import sys
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
import random
import time

def introduce_typo(word):
    if len(word) > 1 and random.random() < 0.2:
        index = random.randint(0, len(word) - 1)
        typo_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
        word = word[:index] + typo_letter + word[index + 1:]
    return word

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver

def setup_database():
    db = sqlite3.connect('instaling.db')
    c = db.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dane (
            polski text, 
            angielski text,
            info text
        )
    ''')
    return db, c

def remove_incomplete_entries(c, db):
    try:
        c.execute("DELETE FROM dane WHERE polski IS NULL OR polski = '' OR angielski IS NULL OR angielski = '' OR info IS NULL OR info = ''")
        db.commit()
    except sqlite3.Error as e:
        print(f"Błąd podczas usuwania niekompletnych wpisów: {e}")

def add_word(driver, c, db, a_polish, info):
    print("Rozpoczynam dodawanie do bazy.")
    remove_incomplete_entries(c, db)

    try:
        try:
            answer = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'answer'))
            )
            answer.clear()
        except Exception as e:
            pass 

        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.ID, 'check'))).click()
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="word"]')))
        
        time.sleep(1) 

        english = driver.find_element(By.XPATH, '//*[@id="word"]').get_attribute("textContent")
        print(f"Slowo po angielsku to: {english}")
        print(f"Slowo po polsku to: {a_polish}")
        
        if english.strip() and a_polish.strip() and info.strip():
            try:
                c.execute("INSERT or IGNORE INTO dane (polski, angielski, info) VALUES (?, ?, ?)", (a_polish, english, info))
                print("Wprowadzam do bazy danych.")
            except sqlite3.IntegrityError:
                print("To slowo już istnieje")
            db.commit()
        else:
            print("Dane są puste, nie dodaję do bazy.")
        
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next_word"]'))).click()
    except Exception as e:
        print(f"Błąd podczas dodawania słowa: {e}")

def start(driver):
    request_element = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="question"]/div[2]/div[2]'))
    )
    info_element = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[8]/div[1]/div[1]'))
    )
    request = request_element.get_attribute("textContent")
    r_info = info_element.get_attribute("textContent")
    
    print(f"Szukane slowo: {request}")
    print(f"Opis slowa to: {r_info}")
    return request, r_info

def check_translation(driver, c, db, request, r_info):
    remove_incomplete_entries(c, db)
    try: 
        knownew_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="know_new"]'))
        )
        knownew_button.click()
        skip_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="skip"]'))
        )
        skip_button.click()
        return "SKIPPED"
    except:
        c.execute("SELECT angielski FROM dane WHERE polski=? and info=?", (request, r_info))
        result = c.fetchone()
        if result:
            print(f"Tlumaczenie to: {result[0]}")
            return result[0]
        else:
            print("Nie mam tlumaczenia.")
            return None

async def run_session(log, pas, number_of_sessions, report_channel_name, mode):
    print(f"Uruchamianie sesji z loginem: {log}, liczbą sesji: {number_of_sessions}, trybem: {mode}")
    
    for i in range(number_of_sessions):
        print(f"--- Rozpoczynanie sesji {i+1} / {number_of_sessions} ---")
        driver = None
        db = None
        try:
            driver = setup_driver()
            db, c = setup_database()
            driver.get("https://instaling.pl/teacher.php?page=login")

            try:
                agree_button = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/button[1]/p'))
                )
                agree_button.click()
            except Exception as e:
                pass

            login = driver.find_element(By.NAME, 'log_email')
            login.send_keys(log)
            passwd = driver.find_element(By.NAME, 'log_password')
            passwd.send_keys(pas)
            passwd.send_keys(Keys.RETURN)
            print("Zalogowano.")

            try:
                x_button_post = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="streak-button-close"]'))
                )
                x_button_post.click()
            except Exception:
                pass

            step_1_success = False
            try:
                session_btn = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.big_button.btn.btn-session.sesion'))
                )
                session_btn.click()
                step_1_success = True

            except Exception as e_session:
                try:
                    daily_session_btn = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, 'Rozpocznij codzienną sesję'))
                    )
                    daily_session_btn.click()
                    step_1_success = True

                except Exception as e_daily:
                    try:
                        next_session_btn = WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.LINK_TEXT, 'Rozpocznij kolejną sesję'))
                        )
                        next_session_btn.click()
                        step_1_success = True
                    
                    except Exception as e_next:
                        try:
                            finish_session_btn = WebDriverWait(driver, 7).until(
                                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Dokończ sesję'))
                            )
                            finish_session_btn.click()
                            step_1_success = True
                            
                        except Exception as e_finish:
                            print(f"Błąd uruchomienia sesji. Nie znaleziono przycisku start.")
                            continue 
                        
            if step_1_success:
                try:
                    continue_btn = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.ID, 'continue_session_button'))
                    )
                    continue_btn.click()
                    print("Rozpoczęto sesję.")
                except Exception as e_continue:
                    try:
                        start_btn = WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.ID, 'start_session_button'))
                        )
                        start_btn.click()
                        print("Rozpoczęto sesję.")
                    except Exception as e_start:
                        print(f"Nie można rozpocząć sesji (błąd krok 2).")
                        continue 

            await asyncio.sleep(random.randint(2, 4))

            while True:
                try:
                    request, r_info = start(driver)
                    translation = check_translation(driver, c, db, request, r_info)
                    
                    if translation and translation != "SKIPPED":
                        
                        original_translation = translation
                        if mode == "human":
                            translation = introduce_typo(translation)
                            if translation != original_translation:
                                print("Wprowadzono celową literówkę...")
                            await asyncio.sleep(random.randint(5, 25))

                        answer = WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.ID, 'answer'))
                        )
                        answer.send_keys(translation)
                        time.sleep(1) 
                        WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.ID, 'check'))
                        ).click()
                        
                        WebDriverWait(driver, 7).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="next_word"]'))
                        ).click()

                        print("---------------------------------------")
                    
                    elif translation is None: 
                        add_word(driver, c, db, request, r_info)
                        print("---------------------------------------")
                    
                    elif translation == "SKIPPED": 
                        print("Pominięto nowe słowo.")
                        print("---------------------------------------")

                    await asyncio.sleep(random.randint(2, 4)) 

                except ElementNotInteractableException:
                    print("Element nie jest interaktywny, kończę sesję.\n### Koniec sesji ###")
                    break
                except Exception as e:
                    print(f"Sesja zakończona (nie znaleziono kolejnego słowa).\n### Koniec sesji ###")
                    break
        
        except Exception as e:
            print(f"Błąd krytyczny podczas konfiguracji sesji: {e}")
        
        finally:
            if driver:
                driver.quit()
            if db:
                db.close()
            print(f"--- Zakończono sesję {i+1} / {number_of_sessions} ---")

if __name__ == "__main__":
    if len(sys.argv) == 6:
        login = sys.argv[1]
        password = sys.argv[2]
        number_of_sessions = int(sys.argv[3])
        report_channel_name = sys.argv[4]
        mode = sys.argv[5]
        asyncio.run(run_session(login, password, number_of_sessions, report_channel_name, mode))
    else:
        print("Niepoprawna liczba argumentów.")
        sys.exit()