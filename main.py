import discord
import dotenv
import os
import asyncio

time_phase0 = 0
time_phase1 = 0
time_phase2 = 0

start_dashboard = f"""

Currently Status
**Phase 0** Checking if self is reachable: ... {time_phase0}
**Phase 1** Checking if Remote Shell is reachable: ... {time_phase1}
**Phase 2** Checking if Public IP is reachable: ... {time_phase2}
                    """


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
                bot_msg = await message.channel.send(start_dashboard)
                asyncio.sleep(5)
                await bot_msg.edit(content="content has been updated\n\n" + start_dashboard)


client.run(priv_token) 
