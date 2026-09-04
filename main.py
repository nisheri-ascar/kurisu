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

dotenv.load_dotenv()
COMMAND_PREFIX = ".katagari"
PRIV_TOKEN = str(os.getenv("TOKEN"))
HOSTED_LINK = str(os.getenv("HOSTED_LINK"))
MC_IP_ADDR = str(os.getenv("MC_IP_ADDR"))
HTTP_PORT = 8080 # FIXME: use envvar
DRY_RUN = bool(os.getenv("DRY_RUN"))
DRY_RUN = False
PRODUCTION_MODE=str(os.getenv("PRODUCTION_MODE"))
GUILD_ID = [1529471469464191057, 1532949516171608236]

if DRY_RUN == True or DRY_RUN == 1:
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

subtext_notes = [f"{st}dev commit: `{commit}`"]

if PRODUCTION_MODE != True:
    subtext_notes.append(f"{st} `PRODUCTION_MODE` is not set. This instance of kurisu is running locally.")
if DRY_RUN == True:
    subtext_notes.append(f"{st} `DRY_RUN` is set to True. Waiting time will be skipped and script will not be executed.")




print(f"Crossed World Line at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} with commit {commit}")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents, debug_guilds=GUILD_ID)
bot.load_extension("cogs.minecraft")

@bot.slash_command(name="ping", description="Check kurisu's latency")
async def ping(ctx: discord.Interaction):
    await ctx.channel.send(f"pong! took {bot.latency} to process!")


@bot.slash_command(name="start", description="Start the Minecraft Server!")
async def start(ctx: discord.Interaction):
    notes = f"\n{"\n".join(subtext_notes)}"
    await ctx.response.defer()
    await ctx.followup.send(f"**Server started**")
    phase_msg = await ctx.channel.send(f"{phase_header_text("inprogress", 1, 3)}: Checking if the script is executable{notes}")
    try:
        if DRY_RUN != True:
            threading.Thread(target=start_script, daemon=True).start()
            # FIXME: when implementing stop command, please make this have some flags.
            # FIXME: add some guard check if the server is started multiple times OR server is in process of starting
    except:
        await phase_msg.edit(f"{phase_header_text("fail", 1, 3)}: Failed to run start script!{notes}")
    else:
        await phase_msg.edit(f"{phase_header_text("success", 1, 3)}: Successfully started script!{notes}")

    await phase_msg.edit(f"{phase_header_text("inprogress", 2, 3)}: checking if i can access the remote shell *({BASE_TIME_WAIT}s)*{notes}")
    await asyncio.sleep(BASE_TIME_WAIT*2)
    async with httpx.AsyncClient() as status:
        try:
            r = await status.get("http://127.0.0.1:6969")
        except:
            await phase_msg.edit(content=f"{phase_header_text("fail", 2, 3)}: Cannot access Remote Shell!{notes}")
        else:
            print("success")
            await phase_msg.edit(content=f"{phase_header_text("success", 2, 3)}: Cloud Server is accessable{notes}")


    await phase_msg.edit(f"{phase_header_text("inprogress", 3, 3)}: Checking Public IP Minecraft Server *({BASE_TIME_WAIT*3}s)* {notes}")
    await asyncio.sleep(BASE_TIME_WAIT*3)
    if check_server_status() == 0:
        await phase_msg.edit(f"{phase_header_text("success", 3, 3)}: Minecraft Server is accessable")
        await ctx.channel.send("**note:** server stops after 3 minutes of no players! be sure to join immediately!")
    else:
        await phase_msg.edit(f"{phase_header_text("fail", 3, 3)}: Minecraft Server is down! Is proxy down? {notes}")

@bot.slash_command(name="check", description="Check minecraft server\'s status")
async def check(ctx: discord.Interaction):
    if check_server_status() == 0:
        await ctx.channel.send(f"checking: Minecraft Server is accessable ")
    else:
        await ctx.channel.send(f"checking: Minecraft Server is down! Is proxy down? ")
        await ctx.channel.send("-# This instance of kurisu environment is running locally.")

@bot.event
async def on_ready():
    print(f"i am {bot.user}")
    threading.Thread(target=http_server, args=(HTTP_PORT,), daemon=True).start()


bot.run(PRIV_TOKEN)

