import sys
import json
import requests
import logging
import datetime
import telebot
import os

os.makedirs("Easy_User/Used", exist_ok=True)

############################### Main Functions ############
def load_login_data():
    try:
        login_data = json.load(open("./Easy_User/Login_data.txt", "r"))

    except:
        with open(f"./Easy_User/Login_data.txt", "w") as login_data_file:
            bot_token = input("Enter Bot Token: ")
            admin = input("Enter Bot admin ID: ")
            domain = input("Enter domain: ")
            port = input("Enter port:")

            login_data = {"bot_token": bot_token,
                          "admin": admin,
                          "domain": domain,
                          "port": port
                          }
            json.dump(login_data, login_data_file)
    return login_data

def get_access_token(pusername, ppassword):
    url = f'https://{domain}:{port}/api/admin/token'
    data = {
        'username': pusername,
        'password': ppassword
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        print("Access token obtained. \n The bot is running...")
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def get_users_list():
    url = f'https://{domain}:{port}/api/users'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        users_list = response.json()["users"]
        users_list = sorted([i["username"] for i in users_list if i["username"].split("_")[0] == "user"])
        return users_list
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving users list: {e}')
        return None

def create_user(vol):
    url = f'https://{domain}:{port}/api/user'
    protocol_ = {'vless': {'flow': 'xtls-rprx-vision'}}
    current_time = datetime.datetime.now()
    date = current_time + datetime.timedelta(days=30)
    expire = int(date.timestamp())
    data_limit = vol * pow(1024, 3)

    users_list = get_users_list()
    if users_list:
        username = "user_" + "{:04d}".format(len(users_list))
    else:
        username = "user_0000"


    user = {
        "username": username,
        "proxies":
            protocol_,
        "inbounds": {
            "vless": [
                "VLESS TCP REALITY"
            ]
        },
        "expire": expire,
        "data_limit": data_limit,
        "data_limit_reset_strategy": "no_reset",
        "note": ""
    }

    try:
        response = requests.post(url, json=user, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while creating user: {e}')
        return None




############ Main Body #####################

login_data = load_login_data()
bot_token = login_data["bot_token"]
admin = login_data["admin"]
domain = login_data["domain"]
port = login_data["port"]
pusername = input("Enter Username: ")
ppassword = input('Enter Password: ')


############# Bot ##########################
bot = telebot.TeleBot(bot_token)

key = telebot.types.ReplyKeyboardMarkup(resize_keyboard= True, row_width= 2)
key.add("10 GB", "15 GB", "20 GB", "30 GB", "40 GB", "50 GB", "100 GB")
def load_auth_file():
    try:
        authorized_users = json.load(open(f"./Easy_User/Authorized_users.txt", "r"))

    except:
        authorized_users = {"admin": int(admin)}
        with open(f"./Easy_User/Authorized_users.txt", "w") as auth_file:

            json.dump(authorized_users, auth_file)

    authorized_users = {y: x for x, y in authorized_users.items()}
    return authorized_users


def authorized_only(func):


    def wrapper(message):
        authorized_users = load_auth_file()

        if message.from_user.id in authorized_users:
            func(message)
        else:
            bot.reply_to(message, "Sorry, you are not authorized to use this command.")
    return wrapper

@bot.message_handler(commands=['start'])
@authorized_only
def welcome(message):
    bot.send_message(message.chat.id, "Welcome. Choose Volume: ", reply_markup=key)

@bot.message_handler(func=lambda message: True, content_types=['text'])
@authorized_only
def prompt(message):
    authorized_users = load_auth_file()
    username = authorized_users[message.chat.id]

    if message.text in ["10 GB", "15 GB", "20 GB", "25 GB", "30 GB", "40 GB", "50 GB", "100 GB"]:
        vol = int(message.text.split(" ")[0])
        user = create_user(vol)
        file1 = open(f"./Easy_User/Used/{username}--v2ray--{vol}-GB.txt", "a+")
        with open(f"./Easy_User/Used/{username}--v2ray--{vol}-GB.txt", "r+") as used:
            num = len(used.readlines()) + 1
            usedline = f"{num}. {user['username']}  {vol}-GB: {user['subscription_url']}"
            used.write(usedline + "\n")
            bot.send_message(admin, f"{username} {vol}-GB \n {usedline}")
            bot.send_message(message.chat.id, usedline)
            used.close()
    else:
        bot.reply_to(message, 'Invalid command')



access_token = get_access_token(pusername, ppassword)
headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
if access_token:
    bot.infinity_polling()
else:
    print("Failed to obtain access token.")
    sys.exit()




