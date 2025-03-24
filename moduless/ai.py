from moduless.base import register_command, register_help, install_module
try:
    import g4f
except ModuleNotFoundError:
    install_module("install -U g4f[all]")

async def gpt(client, message, commandds:dict, config:dict):
    args = message.text.split(" ", 1)
    if len(args) == 2:
        await client.edit_message_text(message.chat.id, message.id, "🕑 Подождите GPT-4o-Mini генерирует ответ...")
        clientgpt = g4f.client.Client()
        response = clientgpt.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": args[1]}],
            web_search=False
        )
        await client.edit_message_text(message.chat.id, message.id, f"🤖 GPT-4o-Mini:\n{response.choices[0].message.content}")
    else:
        await client.edit_message_text(message.chat.id, message.id, "❌ **Неправильно указаны аргументы!**")

async def image(client, message, commandds:dict, config:dict):
    await client.edit_message_text(message.chat.id, message.id, "🕑 Подождите FLUX генерирует ответ...")
    args = message.text.split(" ", 1)
    if len(args) == 2:
        clientgpt = g4f.client.Client()
        response = await clientgpt.images.async_generate(
            model="flux",
            prompt=args[1],
            response_format="url"
        )
        await client.delete_messages(message.chat.id, [message.id])  
        await client.send_photo(message.chat.id, response.data[0].url)
    else:
        await client.edit_message_text(message.chat.id, message.id, "❌ **Неправильно указаны аргументы!**")

# Registration commands:
register_help(
    "AICommands (based on g4f)", #Display name
    "ai", #Short name (allowed chars: "abcdefghijklmnopqrstuvwxyz0123456789" only 12 chars )
    "lunix", #Author
    { # Command helps
        "gpt (prompt)": "Ask GPT-4o-Mini", 
        "image (prompt)": "Generate image using FLUX"
    } 
)
register_command("gpt", gpt)
register_command("image", image)
