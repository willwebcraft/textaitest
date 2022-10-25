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

##########
# VARIABLES
##########
load_dotenv()
xpaths = {
    'toggle_menu': "//div[@id='user-menu']",
    'connexion_btn': '//*[@id="user-menu"]/ul/li[1]/a',
    'login_field' : "//input[@id='user_login']",
    'pwd_field' : "//input[@id='user_password']",
}

class_names = {
    
}

credentials = {
    'email' : os.getenv('MAIL'),
    'pwd' : os.getenv('PWD')
}