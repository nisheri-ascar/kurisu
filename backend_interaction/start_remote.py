import discord
from styling import *
import threading
from datetime import datetime
from server_status import check_server_status
from script_handler import start_script
from config import *
import asyncio
import httpx

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
