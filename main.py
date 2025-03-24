import os
os.system('cls' if os.name=='nt' else 'clear')
print("Importing...")
print("WARNING! PIP MUST BE IN PATH (Windows)\nExample: you can use pip in every folder like open cmd and write pip")
import asyncio
from pyrogram import Client, filters
import json
import time

from moduless.base import handle_message

def purpleblue(text):
    os.system(""); faded = ""
    red = 110
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;255m{line}\033[0m\n")
        if not red == 0:
            red -= 15
            if red < 0:
                red = 0
    return faded


def get_api_id(config):
    if config['api_id'] == "0":
        while True:
            api_id = input("Введите api_id: ")
            if api_id.isdigit():
                return int(api_id)
            else:
                print("Неверный ввод. Пожалуйста, введите числовое значение для api_id.")
    else:
        try:
            return int(config['api_id'])
        except ValueError:
            print("ОШИБКА КОНФИГА! api_id должен быть числом.")
            return None

def save_config(config, filename="config.json"):
    with open(filename, "w") as f:
        json.dump(config, f)

def get_api_hash(config):
    if config['api_hash'] == "0":
        return input("Введите api_hash: ")
    else:
        return config['api_hash']

def load_config(filename="config.json"):
    default_config = {
        "session_name": "lunix",
        "prefix": ".",
        "api_id": "0",
        "api_hash": "0"
    }
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(filename, "w") as f:
            json.dump(default_config, f)
        return default_config


async def main():
    os.system('cls' if os.name=='nt' else 'clear')
    print(purpleblue('''██╗░░░░░██╗░░░██╗███╗░░██╗██╗██╗░░██╗
██║░░░░░██║░░░██║████╗░██║██║╚██╗██╔╝
██║░░░░░██║░░░██║██╔██╗██║██║░╚███╔╝░
██║░░░░░██║░░░██║██║╚████║██║░██╔██╗░
███████╗╚██████╔╝██║░╚███║██║██╔╝╚██╗
╚══════╝░╚═════╝░╚═╝░░╚══╝╚═╝╚═╝░░╚═╝'''))
    config = load_config()
    
    api_id = get_api_id(config)
    if api_id is None:
        return

    api_hash = get_api_hash(config)

    config['api_id'] = api_id
    config['api_hash'] = api_hash

    save_config(config)
    
    session_string = "lunix"
    config['start_time'] = time.time()
    app = Client(session_string, api_id=api_id, api_hash=api_hash)

    @app.on_message(filters.all)
    async def on_message(client, message):
        await handle_message(client, message, config)
    
    await app.start()
    me = await app.get_me()
    print(f"Logged in as {me.first_name} ({me.id})")

    await asyncio.Event().wait()
asyncio.run(main())
