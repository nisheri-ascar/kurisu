import discord
import dotenv
import os
import asyncio
import httpx
from mcstatus import JavaServer
import sys
import subprocess
from datetime import datetime

dotenv.load_dotenv()
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))
MC_IP_ADDR = str(os.getenv("MC_IP_ADDR"))
DEBUG = False

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
    if MC_IP_ADDR == "":
        print("MC_IP_ADDR emtpy!")
        sys.exit(1)

def check_server_status():
    try:
        server = JavaServer.lookup(MC_IP_ADDR)
        status = server.status()
        return 0
    except:
        print("cannot access server!!")
        return 1



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
            # FIXME: move around this one on its own function.
                # process of starting the server starts here
                now = datetime.now()
                await message.channel.send(f"**Server started by {message.author} at {now.strftime("%Y-%m-%d %H:%M:%S")}**")
                try:
                    if DEBUG != True:
                        subprocess.run(["./run-server.sh"])
                    else:
                        pass
                except:
                    await message.channel.send("**🔴 Phase 0**: Failed to run start script!")
                else:
                    await message.channel.send("**🟢 Phase 0**: Successfully started script!")

                #phase 1
                msg = await message.channel.send("**🔶 Phase 1**: checking if i can access the remote shell *(30s)*")
                await asyncio.sleep(30)
                async with httpx.AsyncClient() as status:
                    try:
                        r = await status.get("http://127.0.0.1:6969")
                    except:
                        await msg.edit(content="**🔴 Phase 1**: ERROR, Cannot access Remote Shell!")
                    else:
                        print("success")
                        await msg.edit(content="**🟢 Phase 1**: Cloud Server is accessable")

                # phase 2
                msg = await message.channel.send("**🔶 Phase 2**: Checking Public IP Minecraft Server *(80s)* ")
                await asyncio.sleep(80) 
                if check_server_status() == 0:
                    await msg.edit("**🟢 Phase 2**: Minecraft Server is accessable ")
                else:
                    await msg.edit("**🔴 Phase 2**: Minecraft Server is down! Is proxy down? ")

            elif user_msg[2] == "check":
                # FIXME: Dont Repeat Yourself!
                if check_server_status() == 0:
                    await message.channel.send("**🟢 Phase 2**: Minecraft Server is accessable ")
                else:
                    await message.channel.send("**🔴 Phase 2**: Minecraft Server is down! Is proxy down? ")




check_variables()
client.run(PRIV_TOKEN)
