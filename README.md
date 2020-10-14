# athene-vaalibot
This simple Telegram bot checks the Flarum based [election forum](https://athene.fi/vaalit/) of [Athene](https://athene.fi) (the guild/student association of Information Networks in Aalto University) for new discussions posted under topics regarding nomination of candidates and sends updates to Telegram.
## Setup
```bash
git clone git@github.com:samporapeli/athene-vaalibot.git
cd athene-vaalibot
python3 -m venv venv         # or virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
export VAALI_BOT_TOKEN=your_telegram_token_here
./bot.py
```
