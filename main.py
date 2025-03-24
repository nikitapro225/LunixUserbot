import os
os.system('cls' if os.name=='nt' else 'clear')
print("Importing...")
print("WARNING! PIP MUST BE IN PATH (Windows)\nExample: you can use pip in every folder like open cmd and write pip")
import asyncio
from pyrogram import Client, filters
import json
import time
config = {"session_name": "lunix","prefix": ".","api_id": "","api_hash": ""}
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    with open("config.json", "w") as f:
        json.dump(config, f)
me = {}
config = {}

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

async def main():
    os.system('cls' if os.name=='nt' else 'clear')
    global me, config
    print(purpleblue('''██╗░░░░░██╗░░░██╗███╗░░██╗██╗██╗░░██╗
██║░░░░░██║░░░██║████╗░██║██║╚██╗██╔╝
██║░░░░░██║░░░██║██╔██╗██║██║░╚███╔╝░
██║░░░░░██║░░░██║██║╚████║██║░██╔██╗░
███████╗╚██████╔╝██║░╚███║██║██╔╝╚██╗
╚══════╝░╚═════╝░╚═╝░░╚══╝╚═╝╚═╝░░╚═╝'''))

    
    if config['api_id'] == "":
        cycle = False
        while cycle:
            api_id = input("Введите api_id: ")
            try:
                api_id = int(api_id)
                cycle = False
            except:
                print("invalid ")
                cycle = True
    else:
        api_id = config['api_id']
        try:
            api_id = int(api_id)
        except:
            print("ОШИБКА КОНФИГА!")
    if config['api_id'] == "":
        api_hash = input("Введите api_hash: ")
    else:
        api_hash = config['api_id']
    
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