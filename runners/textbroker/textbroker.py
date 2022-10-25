import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import requests


##########
# METHODS
##########
def send_telegram_msg(message, chat_id):
    print('in send msg telegram')
    url = "https://api.telegram.org/bot{}/".format(os.getenv('BOT_TOKEN'))
    url = url + "sendMessage?text={}&chat_id={}".format(message, chat_id)
    requests.get(url)

def get_chat_id():
    print('get chat id')
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/getUpdates"
    print(requests.get(url).json())

##########
# VARIABLES
##########
load_dotenv()

feutral = os.getenv('FEUTRAL')
porphyre = os.getenv('PORPHYRE')

xpaths = {
    'loginBtn': '//*[@id="navigation"]/div/div/div[2]/a[1]',
    'commandTable': '//tr[3]/td/div[5]/table',
    'categoryLink' : '//tr[3]/td/div[5]/table/tbody/tr[2]/td[1]/a', # add /[i] to browse
    'commandTitle' : '//tr/td[@class="td-a-2 ddrivetip"]/a'
}

class_names = {
    'loginBtn' : 'btn-login'
}

credentials = {
    'email' : os.getenv('MAIL'),
    'pwd' : os.getenv('PWD')
}

commands = {

}


##########
#  INITIALIZE
##########
options = webdriver.ChromeOptions()
options.set_capability("loggingPrefs", {'performance': 'ALL'})
browser = webdriver.Chrome(options=options)
url = os.getenv('TEXTBROKER_URL')

##########
# ACCESSING THE PAGE
##########

browser.get(url)

loginBtn = browser.find_element(By.CLASS_NAME, class_names['loginBtn'])
loginBtn.click()

time.sleep(5)
cookies_button = browser.find_element(By.CLASS_NAME, 'cc-deny')
cookies_button.click()

radio_input = browser.find_element(By.CSS_SELECTOR, 'label[for="userTypeAuthor"')
radio_input.click()

email_field = browser.find_element(By.ID, 'emailInput')
email_field.send_keys(credentials['email'])

pwd_field = browser.find_element(By.ID, 'passwordInput')
pwd_field.send_keys(credentials['pwd'])

login_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
login_button.click()

time.sleep(5)
print('go to commands')
command_button = browser.find_element(By.XPATH, '//td[3]/a')
command_button.click()


##########
# DATA RETRIEVING
##########

# FETCH DATA
raw_command_data = browser.find_elements(By.XPATH, xpaths['categoryLink'])
print(raw_command_data)
for element in raw_command_data:
    print('ELEMENT IS')
    print(element)
    item = element.find_element(By.XPATH, '//b')
    print(item.text)
    commands[item.text] = []

    element.click()

    commandTitles = browser.find_elements(By.XPATH, xpaths['commandTitle'])
    for item in commandTitles:
        commands[item.text].append(item.text)




time.sleep(5)

# PARSE DATA

# COMPARE DATA STATE 

# STORE DATA STATE 

# IF NEW DATA THEN SEND NOTIF WITH TELEGRAM
send_telegram_msg(f'🚀 *NEW DATA HAS ARRIVED* : \nDATA : {commands}', feutral)

time.sleep(5)
browser.quit()