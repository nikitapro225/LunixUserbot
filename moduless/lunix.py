from moduless.base import register_command, register_help, importo
import platform
import time
import psutil
import os
import requests


def format_uptime(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{hours}:{minutes:02}:{int(seconds):02}"

async def info(client, message, commandds:dict, config:dict):
    system = platform.system()

    device = ""
    if system == "Linux":
        if "com.termux" in os.getenv("PREFIX", ""):
            device = "Termux"
        else:
            device = "Linux"
    elif system == "Windows":
        device = "Windows"
    else:
        client.edit_message_text(message.chat.id, message.id, f"Unsupported device!")
    custom_emoji = {
        "lunix": "<emoji id=6266909029247751517>🪐</emoji><emoji id=6264643996639827624>🪐</emoji><emoji id=6264943136817027219>🪐</emoji><emoji id=6264633040178255244>🪐</emoji>",
        "Windows": "<emoji id=6267133540073215268>🤙</emoji><emoji id=6264535746284099345>🤙</emoji><emoji id=6267231680075929714>🤙</emoji><emoji id=6264979502305122076>🤙</emoji>",
        "Linux": "<emoji id=6264672416438424942>🤤</emoji><emoji id=6266835688386204867>🤤</emoji><emoji id=6264740813792613657>🤤</emoji><emoji id=6266826703314621586>🤤</emoji>",
        "Termux": "<emoji id=6266983607059878766>⚠️</emoji><emoji id=6267169330035693038>⚠️</emoji><emoji id=6266939257227580461>⚠️</emoji><emoji id=6264672416438424942>⚠️</emoji>"
    }
    if bool(message.from_user.is_premium) == True or message.chat.id == message.from_user.id:
        text = f'''{custom_emoji["lunix"]}

<emoji id=5386828444560530381>😼</emoji> **Владелец:** {message.from_user.first_name if not message.from_user.username else f"[{message.from_user.first_name}](https://t.me/{message.from_user.username})"}
<emoji id=5372981976804366741>🤖</emoji> **Префикс:** «{config["prefix"]}»
<emoji id=5370869711888194012>👾</emoji> **Аптайм:** {format_uptime(time.time() - config['start_time'])}

{custom_emoji[device]}

<emoji id=5431376038628171216>💻</emoji> **Использование CPU:** {psutil.Process().cpu_percent(interval=1)}%
<emoji id=5470049770997292425>🌡</emoji> **Использование RAM:** {round(psutil.Process().memory_info().rss / (1024 * 1024))}MB'''
        await client.delete_messages(message.chat.id, [message.id])
        await client.send_photo(message.chat.id, "lunix.png", caption=text, reply_to_message_id=message.reply_to_message_id if message.reply_to_message_id else None)
        #await client.edit_message_text(message.chat.id, message.id, text, parse_mode=None)
    elif bool(message.from_user.is_premium) == False:
        text = f'''**Lunix Userbot**

😼 **Владелец:** {message.from_user.first_name if not message.from_user.username else f"[{message.from_user.first_name}](https://t.me/{message.from_user.username})"}
🤖 **Префикс:** «{config["prefix"]}»
👾 **Аптайм:** {format_uptime(time.time() - config['start_time'])}

{device}

💻 **Использование CPU:** {psutil.Process().cpu_percent(interval=1)}%
🌡 **Использование RAM:** {round(psutil.Process().memory_info().rss / (1024 * 1024))}MB'''
        await client.delete_messages(message.chat.id, [message.id])
        await client.send_photo(message.chat.id, "lunix.png", caption=text, reply_to_message_id=message.reply_to_message_id if message.reply_to_message_id else None)

async def helpe(client, message, commandds:dict, config:dict):
    args = message.text.split(" ")
    if len(args) == 2:
        text = f"**😋 Помощь по модулю {args[1]}: **\n"
        for commanda in commandds[args[1]]['command_help']:
            text += f"\n**{commanda}** - {commandds[args[1]]['command_help'][commanda]}"
        await client.edit_message_text(message.chat.id, message.id, text, parse_mode=None)
    else:
        text = "**😋 Список команд: **\n"
        for modulelist in commandds:
            text += f"\n**{modulelist}** от **{commandds[modulelist]['author']}** - {modulelist}"
        text += "\n\n😎 Чтобы узнать команды от модуля введите .help <короткое имя>\nПример: .help ai"
        await client.edit_message_text(message.chat.id, message.id, text, parse_mode=None)

async def dlm(client, message, commandds:dict, config:dict):
    args = message.text.split(" ")
    if len(args) == 2:
        if len(args[1]) > 12 or len(args[1]) < 2:
            await client.edit_message_text(message.chat.id, message.id, "❌ **Unsupported name**")
            return
        allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        register = True
        for i in list(args[1]):
            if i in allowed_chars:
                pass
            else:
                register = False
        if register == False:
            await client.edit_message_text(message.chat.id, message.id, "❌ **Unsupported name**")
            return
        if args[1] in commandds:
            await client.edit_message_text(message.chat.id, message.id, "❌ **Модуль уже установлен!**")
            return
        else:
            await client.edit_message_text(message.chat.id, message.id, f"🕑 **Установка модуля `{args[1]}`...**")
            reqq = requests.get(f"https://raw.githubusercontent.com/nikitapro225/LunixLibrary/refs/heads/main/modules/{args[1]}.py")
            if reqq.status_code == 200:
                with open(f"moduless/{args[1]}.py", "w", encoding='utf-8') as f:
                    f.write(reqq.text)
                await client.edit_message_text(message.chat.id, message.id, f"👍 **Модуль `{args[1]}` успешно установлен!**")
                importo(args[1])
            else:
                await client.edit_message_text(message.chat.id, message.id, "❌ **Модуль не найден**")
    else:
        await client.edit_message_text(message.chat.id, message.id, "❌ **Неправильно указаны аргументы!**")

async def ping(client, message, commandds:dict, config:dict):
    start = time.time()
    await client.edit_message_text(message.chat.id, message.id, "⚡️")
    end = time.time()
    latency = (end - start) * 1000 
    if message.from_user.is_premium == True or message.chat.id == message.from_user.id:
        await client.edit_message_text(message.chat.id, message.id, f"<emoji id=5431449001532594346>⚡️</emoji> **Скорость отклика Telegram: `{round(latency, 3)}` ms**")

        
    else:
        await client.edit_message_text(message.chat.id, message.id, f"⚡️ **Скорость отклика Telegram: `{round(latency, 3)}` ms**")
        
register_help("Main LUNIX", "main", "lunix", {"info": "Get info about LUNIX", "help": "Get help about", "dl (short name)": "Downloads module from [repo](https://github.com/nikitapro225/LunixLibrary/)"})
register_command("info", info)
register_command("help", helpe)
register_command("dl", dlm)
register_command("ping", ping)