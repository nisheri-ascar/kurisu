import discord
import dotenv
import os
import asyncio
import httpx
from mcstatus import JavaServer
import sys
import subprocess
from datetime import datetime
import http.server
import socketserver
import functools
import threading


dotenv.load_dotenv()
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))
MC_IP_ADDR = str(os.getenv("MC_IP_ADDR"))
HTTP_PORT = 8080 # FIXME: use envvar
DRY_RUN = str(os.getenv("DRY_RUN"))
BASE_TIME_WAIT=30
httpd = None
global version
try:
    file_commit = open("/version", 'r')
    commit = file_commit.read()
except FileNotFoundError as err:
    print("can't find commit.")
    commit = "???"


now = datetime.now()
print(f"Crossed World Line at {now.strftime("%Y-%m-%d %H:%M:%S")} with commit {commit}")
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

def http_server():
    global httpd
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="./website")
    httpd = socketserver.TCPServer(("", HTTP_PORT), Handler)
    print("Server at port: ", HTTP_PORT)
    httpd.serve_forever()

def start_script():
    subprocess.run(["./run-server.sh"])


@client.event
async def on_ready():
    print(f"i am {client.user}")
    threading.Thread(target=http_server, daemon=True).start()

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
            await message.channel.send("WIP")
        elif user_msg[1] == "ping":
            await message.channel.send("pong!")

        elif user_msg[1] == "server":
            if user_msg[2] == "start":
            # FIXME: move around this one on its own function.
                # process of starting the server starts here
                now = datetime.now()
                await message.channel.send(f"**Server started by {message.author} at {now.strftime("%Y-%m-%d %H:%M:%S")}**\n-# dev commit: `{commit}`")
                try:
                    if DRY_RUN != True:
                        threading.Thread(target=start_script, daemon=True).start()
                        # FIXME: when implementing stop command, please make this have some flags.
                        # FIXME: add some guard check if the server is started multiple times OR server is in process of starting
                    else:
                        pass
                except:
                    await message.channel.send("**🔴 Phase 0**: Failed to run start script!")
                else:
                    await message.channel.send("**🟢 Phase 0**: Successfully started script!")

                #phase 1
                msg = await message.channel.send(f"**🔶 Phase 1**: checking if i can access the remote shell *({BASE_TIME_WAIT}s)*")
                await asyncio.sleep(BASE_TIME_WAIT*2)
                async with httpx.AsyncClient() as status:
                    try:
                        r = await status.get("http://127.0.0.1:6969")
                    except:
                        await msg.edit(content="**🔴 Phase 1**: ERROR, Cannot access Remote Shell!")
                    else:
                        print("success")
                        await msg.edit(content="**🟢 Phase 1**: Cloud Server is accessable")

                # phase 2
                msg = await message.channel.send(f"**🔶 Phase 2**: Checking Public IP Minecraft Server *({BASE_TIME_WAIT*3}s)* ")
                await asyncio.sleep(BASE_TIME_WAIT*3)
                if check_server_status() == 0:
                    await msg.edit("**🟢 Phase 2**: Minecraft Server is accessable ")
                    await message.channel.send("**note:** server stops after 3 minutes of no players! be sure to join immediately!")
                else:
                    await msg.edit("**🔴 Phase 2**: Minecraft Server is down! Is proxy down? ")

            elif user_msg[2] == "check":
                # FIXME: Dont Repeat Yourself!
                if check_server_status() == 0:
                    await message.channel.send("**🟢 Phase 2**: Minecraft Server is accessable ")
                else:
                    await message.channel.send("**🔴 Phase 2**: Minecraft Server is down! Is proxy down? ")
            elif user_msg[2] == "stop":
                await message.channel.send("not implemented **(yet!)**")


check_variables()
try:
    client.run(PRIV_TOKEN)
except KeyboardInterrupt as e:
    print(f"exiting as stated from {e}")
    sys.exit(0)
