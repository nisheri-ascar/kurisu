import discord
from discord.ext import commands
import dotenv
import os
import sys
from datetime import datetime
from config import *
from styling import *
from dummy_http import http_server
import threading

print(f"Crossed World Line at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} with commit {commit}")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=intents, debug_guilds=GUILD_ID)
bot.load_extension("cogs.minecraft")

@bot.event
async def on_ready():
    print(f"i am {bot.user}")
    threading.Thread(target=http_server, args=(HTTP_PORT,), daemon=True).start()


bot.run(PRIV_TOKEN)

