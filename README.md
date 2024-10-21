# athene-vaalibot
This simple Telegram bot checks the Flarum based [election forum](https://vaalit.athene.fi/) of [Athene](https://athene.fi) (the guild/student association of Information Networks in Aalto University) for new discussions posted under topics regarding nomination of candidates and sends updates to Telegram.
## Setup
```bash
git clone git@github.com:athenekilta/athene-vaalibot.git
cd athene-vaalibot
python3 -m venv venv         # or virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
# "legacy" bot (sends messages to multiple chats)
export VAALI_BOT_TOKEN=your_telegram_token_here
./bot.py
# channel bot (only sends message to one chat/channel)
VAALI_BOT_TOKEN=your_telegram_token_here VAALI_BOT_CHAT_ID=channel_chat_id_here ./channel_bot.py
```

Channel bot exits after going through the candidate lists and sending updates.
Scheduled runs e.g. using `cron` are the recommended way to run the channel bot.

## Credits

This bot is a fork of [Sampo Rapeli's original athene-vaalibot](https://github.com/samporapeli/athene-vaalibot), initially created by [Sampo Rapeli](https://github.com/samporapeli).