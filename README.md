# Marzban_Easy_User
ㅤ

## Installation
First install:
```
sudo apt install python3-pip -y && pip install pytelegrambotapi
```

Then run this command:

```
wget https://raw.githubusercontent.com/sons-of-liberty/Marzban_Easy_User/main/main.py && python3 main.py

```

## Features

- Create users from ready-made templates.
- Add resellers and keep number of users created by them.
- Notify Admin whenever a new user is created.

## How-to
### Login_Data
When you first run the bot, it asks you for the following: 

   [`Telegram bot token, Telegram bot admin ID, Panel Domain, Panel port, Panel admin username, Panel admin password`]

   
The first four are saved into a text file for later use (inside `Login_Data.txt`, but the last two arent saved anywhere. Therefore you are asked to enter panel username and password, everytime you run the bot. 

### Authorized users
There is another file called 'Authorized_users.txt`, which is also a python dictionary, inside which telegram admins can be defined. To define new admins, add them like this: 

`
{"admin": xxxxxxxxx,
"admin2": xxxxxxxxx,
"admin3": xxxxxxxxx}
`
where `xxxxxxxxx` is the numerical ID associated with each telegram account. 


### Used folder
Inside this folder, you will find text files which are used as a simple accounting tool to help you manage your resellers. The files are named based on resellers' names and the data limit set for each user.

For example: `admin3--v2ray--50-GB.txt` holds all 50 GB users created by admin3. If you want to zero the counts, simply remove these text files. 




  
  

## Donation
If you found this bot helpful and would like to support me, you can send your donations to:
- TRON network (TRC20): `TK28Znv9VWF8M9qAZsFHH7EkSVZyKKyZ1v`

Thank You. 
ㅤ
