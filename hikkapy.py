import hikka

TOKEN = "TOKEN"

client = hikka.Client(Token=TOKEN)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    
@client.event
async def on_message(message):
    if message.content.startswith("!Hello"):
        await message.reply("Hello, world!")
        
@client.event
async def on_message_edit(before, after):
    pass

@client.event
async def on_message_delete(message):
    pass

client.run()