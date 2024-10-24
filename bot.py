#!/usr/bin/env python3

import json
import os
import sys
import requests
import telebot
import threading
import time

try:
    token = os.environ["VAALI_BOT_TOKEN"]
except KeyError:
    print("You must set VAALI_BOT_TOKEN environment variable (export VAALI_BOT_TOKEN=your_telegram_token)")
    sys.exit(1)

bot = telebot.TeleBot(token, parse_mode="MARKDOWN")

max_requests_per_second = 30
required_delay = 1 / max_requests_per_second

with open("data.json", "r") as datafile:
    data = json.load(datafile)

def save_data():
    with open("data.json", "w") as datafile:
        json.dump(data, datafile)

@bot.message_handler(commands=["help"])
def help_message(message):
    with open("telegram/description.txt", "r") as description_file:
        description = description_file.readlines()
    with open("telegram/commands.txt", "r") as commands_file:
        commands = commands_file.readlines()
    response_text = "".join(description + ["\n"] + ["/" + line for line in commands])
    bot.reply_to(message, response_text)

@bot.message_handler(commands=["start"])
def start_bot(message):
    if message.chat.id not in data["active_chats"]:
        data["active_chats"].append(message.chat.id)
        save_data()
    bot.reply_to(message, "Hienoa, yritän nyt muistaa ilmoittaa, jos joku asettuu ehdolle!")

@bot.message_handler(commands=["stop"])
def stop_bot(message):
    if message.chat.id in data["active_chats"]:
        del data["active_chats"][data["active_chats"].index(message.chat.id)]
        save_data()
    bot.reply_to(message, "En enää laita ilmoituksia tähän ryhmään, ellet lähetä minulle /start uudelleen.")

@bot.message_handler(commands=["tilanne"])
def situation(message):
    response_text = ""
    for election_list in data["config"]["lists"]:
        list_link = f"[{election_list['name']}]({election_list['user_url']})"
        response_text += f"{list_link}: {str(election_list['last_count'])}\n"
    response_text += "Tarkemmat tiedot: https://vaalit.athene.fi/"
    bot.reply_to(message, response_text)

thread = threading.Thread(target=bot.polling)
thread.daemon = True
thread.start()

print("Bot started, watching for changes")
while True:
    try:
        for election_list in data["config"]["lists"]:
            api_response = json.loads(requests.get(election_list["api_url"]).text)
            new_count = len(api_response["data"])
            while "next" in api_response["links"]:
                api_response = json.loads(requests.get(api_response["links"]["next"]).text)
                new_count += len(api_response["data"])
            if new_count > election_list["last_count"]:
                print(f"{time.strftime('%T')}: {new_count} > {election_list['last_count']}: {election_list['change_text']}")
                before_send_time = time.time()
                previous_request_start = time.time() - required_delay
                for chat_id in data["active_chats"]:
                    sleep_time = max(0, required_delay - (time.time() - previous_request_start))
                    time.sleep(sleep_time)
                    previous_request_start = time.time()
                    try:
                        bot.send_message(chat_id, election_list["change_text"] + "\n" + election_list["user_url"])
                    except:
                        print("Unable to send to chat " + str(chat_id))
                time_taken = time.time() - before_send_time
                print(f"Messages sent in {time_taken} seconds ({len(data['active_chats'])/time_taken} requests/second)")
            election_list["last_count"] = new_count
            save_data()
    except:
        print("Error, waiting and trying again")
        time.sleep(30)
    time.sleep(10)
