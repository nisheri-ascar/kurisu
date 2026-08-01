import discord
import dotenv
import os

dotenv.load_dotenv()
priv_token = str(os.getenv("TOKEN"))
print(priv_token)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"i am {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$kurisu"):
        await message.channel.send("Run `$kurisu help` for more info")
    elif message.content.startswith("$kurisu server start"):
        await message_channel.send("""
            Phase 0: Checking if self is up...
            Phase 1: Testing remote shell is accessible.
            Phase 2: Testing if Public IP is acce


            """)

client.run(priv_token) 
