# moduless/base.py
import os
import importlib

commands = {}
helper = {}

def register_command(name, func):
    commands[name] = func

def register_help(name : str, short_name:str, author : str, commands : dict):
    allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    register = True
    for i in list(short_name):
        if i in allowed_chars:
            pass
        else:
            register = False
    if len(short_name) > 12 or len(short_name) < 2:
        register = False
    if register == False:
        return
    helper[short_name] = {"command_help": commands, "author": author, "name": name}

def install_module(call:str):
    os.system("pip "+call)

package_name = __name__.rsplit('.', 1)[0]
package_dir = os.path.dirname(__file__)
importlib.import_module(f"{package_name}.lunix")
def importo(modulka):
    importlib.import_module(f"{package_name}.{modulka}")

async def handle_message(client, message, config:dict):
    if message.from_user and message.from_user.is_self:
        if message.text and message.text.startswith('.'):
            parts = message.text[1:].split()
            command_name = parts[0]
            args = parts[1:]
            
            if command_name in commands:
                await commands[command_name](client, message, helper, config)
            else:
                await client.edit_message_text(message.chat.id, message.id, "❌ **Команда не найдена!**")

for module in os.listdir(package_dir):
    
    if module.endswith('.py') and not module in ['__init__.py', "lunix.py"]:
        module_name = module[:-3]
        importlib.import_module(f"{package_name}.{module_name}")