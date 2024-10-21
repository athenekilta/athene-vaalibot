#!/usr/bin/env python3

import json
import os
import requests
import sys
import telebot
from datetime import datetime

try:
    token = os.environ["VAALI_BOT_TOKEN"]
    chat_id = os.environ["VAALI_BOT_CHAT_ID"]
except KeyError:
    print("You must set VAALI_BOT_TOKEN and VAALI_BOT_CHAT_ID environment variables")
    sys.exit(1)

def log(message):
    print(f"{datetime.now()}: {message}")

bot = telebot.TeleBot(token, parse_mode="MARKDOWN")

def load_data():
    with open("data.json", "r") as datafile:
        return json.load(datafile)

def save_data(data):
    with open("data.json", "w") as datafile:
        json.dump(data, datafile)

def situation():
    response_text = ""
    for election_list in load_data()["config"]["lists"]:
        list_link = f"[{election_list['name']}]({election_list['user_url']})"
        response_text += f"{list_link}: {str(election_list['last_count'])}\n"
    response_text += "More information on the forum: https://vaalit.athene.fi/"
    return response_text

new_posts = False
load_data()
log("Going through election lists")
data = load_data()
for election_list in data["config"]["lists"]:
    log(f"Current list: {election_list['name']}")
    api_response = json.loads(requests.get(election_list["api_url"]).text)
    new_count = len(api_response["data"])
    while "next" in api_response["links"]:
        api_response = json.loads(requests.get(api_response["links"]["next"]).text)
        new_count += len(api_response["data"])
    if new_count > election_list["last_count"]:
        new_posts = True
        log(f"{new_count} > {election_list['last_count']}: {election_list['change_text']}")
        bot.send_message(chat_id, election_list["change_text"] + "\n" + election_list["user_url"])
    election_list["last_count"] = new_count
    save_data(data)
if new_posts: bot.send_message(chat_id, situation())
