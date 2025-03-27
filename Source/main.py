# в случае наличии лицензии на 2Captcha API вы можете в функцию captcha() вставить код из readMe.txt 
from twocaptcha import TwoCaptcha
import twocaptcha

# Используется для отслеживания нажатия горячей клавиши
from pynput import keyboard
import threading

# Используется для взаимодействия с вашего браузером
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Используется для создания задержек, чтобы страницы успевали загрузиться
import time

stop_listener = False
hotkey_pressed = False

def on_press(key):
    global hotkey_pressed, stop_listener
    try:
        if key.char == 'q' or key.char == 'й':
            hotkey_pressed = True
            print("Горячая клавиша нажата - завершаем диалог")
    except AttributeError:
        pass

def keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def captcha():
    time.sleep(0.75)
    try:
        recaptcha = driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]')
        if recaptcha:
            recaptcha.click()
    except Exception as e:
        print('Пожалуйста, пройдите капчу')


def find_and_click_end_button():
    try:
        try:
            first_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Завершить")]'))
            )
            driver.execute_script("arguments[0].click();", first_button)
            print("Первая кнопка 'Завершить' нажата")
            time.sleep(1)

            confirm_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm')]"))
            )
            driver.execute_script("arguments[0].click();", confirm_button)
            print("Кнопка подтверждения нажата")
            time.sleep(1)
        except:
            print("Кнопка 'Завершить' не найдена, возможно собеседник уже завершил разговор")

        new_chat_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Начать новый разговор")]'))
        )
        driver.execute_script("arguments[0].click();", new_chat_button)
        print("Кнопка 'Начать новый разговор' нажата")
        
        return True
        
    except NoSuchElementException:
        print("Ни одна из кнопок не найдена")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
        
    except NoSuchElementException:
        print("Одна из кнопок не найдена")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

        
    except NoSuchElementException:
        print("Кнопка 'Завершить' не найдена")
        return False
    except Exception as e:
        print(f"Ошибка при нажатии кнопки 'Завершить': {e}")
        return False


listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.daemon = True
listener_thread.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--use-fake-ui-for-media-stream")

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://nekto.me/audiochat#/peer')
time.sleep(2)

sex = driver.find_element(By.XPATH, '//*[contains(text(), "М")]')
sex.click()
time.sleep(0.25)

age = driver.find_element(By.XPATH, '//*[contains(text(), "от 18 до 24 лет")]')
age.click()
time.sleep(0.25)

button = driver.find_element(By.ID, 'searchCompanyBtn')
button.click()
time.sleep(0.75)
captcha()

try:
    while True:
        if hotkey_pressed:
            if find_and_click_end_button():
                hotkey_pressed = False
                captcha()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Скрипт остановлен пользователем")
finally:
    driver.quit()