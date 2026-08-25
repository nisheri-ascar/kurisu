import discord
from discord.ext import commands
import dotenv
import os
import asyncio
import httpx
import sys
from datetime import datetime
from dummy_http import http_server
from server_status import check_server_status
from script_handler import start_script
from styling import *
import threading

global version

       # elif user_msg[1] == "ping":
dotenv.load_dotenv()
COMMAND_PREFIX = ".katagari"
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))
MC_IP_ADDR = str(os.getenv("MC_IP_ADDR"))
HTTP_PORT = 8080 # FIXME: use envvar
#DRY_RUN = str(os.getenv("DRY_RUN"))
DRY_RUN = True
PRODUCTION_MODE=str(os.getenv("PRODUCTION_MODE"))
GUILD_ID = 1529471469464191057

if DRY_RUN == True:
    BASE_TIME_WAIT = 0
else:
    BASE_TIME_WAIT=30
httpd = None

try:
    file_commit = open("/version", 'r')
    commit = file_commit.read()
except FileNotFoundError as err:
    print("can't find commit.")
    commit = "???"


print(f"Crossed World Line at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} with commit {commit}")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intent=intents)

@bot.tree.command(name="start", description="Start the Minecraft server!")
async def start(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send("hello world from newer framework!!")

@bot.event
async def on_ready():
    print(f"i am {bot.user}")
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    threading.Thread(target=http_server, args=(HTTP_PORT,), daemon=True).start()

@bot.event
async def on_message(message):
    print(f"{message.author} | {message.content}")
    #if message.author == client.user:
     #   return

    if message.content.startswith(COMMAND_PREFIX):
        print(message.content)
        user_msg = message.content.split(" ")
        print(user_msg)
        if user_msg[1] == "help":
            commands.help(message)
        elif user_msg[1] == "ping":
            commands.ping(message)
        elif user_msg[1] == "server":
            if user_msg[2] == "start":
            # FIXME: move around this one on its own function.
                # process of starting the server starts here
                now = datetime.now()
                await message.channel.send(f"**Server started by {message.author} at {now.strftime("%Y-%m-%d %H:%M:%S")}**\n-# dev commit: `{commit}`")
                if PRODUCTION_MODE == False:
                    pass
                try:
                    PHASE_LEVEL = 0
                    if DRY_RUN != True:
                        threading.Thread(target=start_script, daemon=True).start()
                        # FIXME: when implementing stop command, please make this have some flags.
                        # FIXME: add some guard check if the server is started multiple times OR server is in process of starting
                    else:
                        await message.channel.send(f"{b}DRY_RUN is set to True. Waiting time will be skipped and script will not be ran.{b}")
                except:
                    await message.channel.send(f"{b}{PHASE_ERROR}{PHASE_LEVEL}{b}: Failed to run start script!")
                else:
                    await message.channel.send(f"{b}{PHASE_DONE}{PHASE_LEVEL}{b}: Successfully started script!")

                #phase 1
                PHASE_LEVEL = 1
                msg = await message.channel.send(f"{b}{PHASE_PROGRESS}{PHASE_LEVEL}{b}: checking if i can access the remote shell *({BASE_TIME_WAIT}s)*")
                await asyncio.sleep(BASE_TIME_WAIT*2)
                async with httpx.AsyncClient() as status:
                    try:
                        r = await status.get("http://127.0.0.1:6969")
                    except:
                        await msg.edit(content=f"{b}{PHASE_ERROR}{PHASE_LEVEL}{b}: Cannot access Remote Shell!")
                    else:
                        print("success")
                        await msg.edit(content=f"{b}{PHASE_DONE}{PHASE_LEVEL}{b}: Cloud Server is accessable")

                # phase 2
                PHASE_LEVEL = 2
                msg = await message.channel.send(f"{b}{PHASE_PROGRESS}{PHASE_LEVEL}{b}: Checking Public IP Minecraft Server *({BASE_TIME_WAIT*3}s)* ")
                await asyncio.sleep(BASE_TIME_WAIT*3)
                if check_server_status() == 0:
                    await msg.edit(f"{b}{PHASE_DONE}{PHASE_LEVEL}{b}: Minecraft Server is accessable ")
                    await message.channel.send("**note:** server stops after 3 minutes of no players! be sure to join immediately!")
                else:
                    await msg.edit(f"{b}{PHASE_ERROR}{PHASE_LEVEL}{b}: Minecraft Server is down! Is proxy down? ")

            elif user_msg[2] == "check":
                # FIXME: Dont Repeat Yourself!
                if check_server_status() == 0:
                    await message.channel.send(f"checking: Minecraft Server is accessable ")
                else:
                    await message.channel.send(f"checking: Minecraft Server is down! Is proxy down? ")
                    await message.channel.send("-# This instance of kurisu environment is running locally.")
            elif user_msg[2] == "stop":
                await message.channel.send("not implemented **(yet!)**")



bot.run(PRIV_TOKEN)

