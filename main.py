import discord
import dotenv
import os
import asyncio
import httpx



dotenv.load_dotenv()
priv_token = str(os.getenv("TOKEN"))

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
                msg = await message.channel.send("phase 0: checking if i can access myself 🔶")
                async with httpx.AsyncClient() as status:
                    r = await status.get("https://www.google.com")
                    print(r.status_code)
                    if r.status_code == 200:
                        print("success")
                        await msg.edit(content="phase 0: okay, i can access myself 🟢")





client.run(priv_token) 
