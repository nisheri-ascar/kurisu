import discord
import dotenv
import os
import asyncio
import httpx
import mcstatus
import sys

dotenv.load_dotenv()
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))
IP_ADDR = "mc.hypixel.net" # FIXME: make this on .env file.


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def check_variables():
    if PRIV_TOKEN == "":
        print("token empty!")
        sys.exit(1)
    if HOSTED_LINK == "":
        print("HOSTED_LINK empty!")
        sys.exit(1)
    if IP_ADDR == "":
        print("IP_ADDR emtpy!")
        sys.exit(1)

def check_server_status():
    # this is syncronous code, pls check later if this actually works inside async
    try:
        server = JavaServer.lookup(IP_ADDR)
        status = server.status()
    except:
        print("cannot access server!!")

@client.event
async def on_ready():
    print(f"i am {client.user}")

@client.event
async def on_message(message):
    print(f"{message.author} | {message.content}")
    #if message.author == client.user:
     #   return

    if message.content.startswith(".kurisu"):
        print(message.content)
        user_msg = message.content.split(" ")
        print(user_msg)
        if user_msg[1] == "help":
            await message.channel.send("todo: help")
        elif user_msg[1] == "server":
            if user_msg[2] == "start":
                # process of starting the server starts here
                await message.channel.send("starting server!")
                # phase 0 self check
                
                msg = await message.channel.send("phase 0: checking if i can access myself 🔶")
                async with httpx.AsyncClient() as status:
                    await asyncio.sleep(1)
                    try:
                        r = await status.get(HOSTED_LINK)
                    except:
                        await msg.edit("phase 0: ERROR! I can't access myself!❗❗❗")
                    else:
                        await msg.edit(content="phase 0: okay, i can access myself 🟢")

                #phase 1 remote shell
                msg = await message.channel.send("phase 1: checking if i can access the remote shell 🔶")
                async with httpx.AsyncClient() as status:
                    await asyncio.sleep(1) # change me to 60 later
                    try:
                        r = await status.get("http://localhost:8080")
                    except:
                        await msg.edit(content="phase 1: ERROR, I can't access the remote shell! ❗❗❗")
                    else:
                        print("success")
                        await msg.edit(content="phase 1: okay, i can access the remote shell 🟢")




check_variables()
client.run(PRIV_TOKEN)