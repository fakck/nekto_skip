# в случае наличии лицензии на 2Captcha API вы можете в функцию captcha() вставить код из readMe.txt 
from twocaptcha import TwoCaptcha
import twocaptcha

# Используется для отслеживания нажатия горячей клавиши
from pynput import keyboard
import threading

# Используется для взаимодействия с вашим браузером
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Используется для создания задержек, чтобы страницы успевали загрузиться
import time
    
def captcha():
    time.sleep(1.5)
    try:
        recaptcha = driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]')
        recaptcha.click()
    except Exception as e:
        print('Пожалуйста, пройдите капчу (у нас не получилось)')
    

def press_bind():
    try:
        end_call = driver.find_element(By.XPATH, '//*[contains(text(), "Завершить")]')
        next_call = driver.find_element(By.XPATH, '//*[contains(text(), "Начать новый разговор")]')
        end_call.click()
        next_call.click()
    except Exception as e:
        print(f'Ошибка при переключении на следующего собеседника: {e}')

def on_press(key):
    try:
        if key == keyboard.Key.f1:
            press_bind()
    except AttributeError:
        pass

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

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
time.sleep(1)

age = driver.find_element(By.XPATH, '//*[contains(text(), "до 17 лет")]')
age.click()
time.sleep(1)

button = driver.find_element(By.ID, 'searchCompanyBtn')
button.click()
time.sleep(1)

while driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]'): # type: ignore
    captcha()

keyboard_thread = threading.Thread(target=start_keyboard_listener)
keyboard_thread.daemon = True
keyboard_thread.start()



time.sleep(10000)