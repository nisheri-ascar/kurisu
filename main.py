import discord
import dotenv
import os
import asyncio
import httpx

dotenv.load_dotenv()
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

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
                    r = await status.get("https://www.google.com")
                    print(r.status_code)
                    if r.status_code == 200:
                        print("success")
                        await msg.edit(content="phase 0: okay, i can access myself 🟢")
                    else:
                        print(f"error {r.status_code}")


                #phase 1 remote shell
                msg = await message.channel.send("phase 1: checking if i can access the remote shell 🔶")
                async with httpx.AsyncClient() as status:
                    await asyncio.sleep(60)
                    r = await status.get("http://localhost:8080")
                    print(r.status_code)
                    if r.status_code == 200:
                        print("success")
                        await msg.edit(content="phase 1: okay, i can access the remote shell 🟢")
                    else:
                        print(f"error {r.status_code}")
                        await msg.edit(content="phase 1: ERROR, I can't access the remote shell! ❗❗❗")






client.run(PRIV_TOKEN) 
