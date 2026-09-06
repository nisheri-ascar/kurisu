import discord
from discord.ext import commands
from backend_interaction import start_remote
from server_status import check_server_status

class Minecraft(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@discord.slash_command(name="test", description="test")
	async def test(self, ctx):
		await ctx.respond("test complete!")

	minecraft = discord.SlashCommandGroup("minecraft", "Minecraft stuff (change me!!)")

	server = minecraft.create_subgroup("server", "todo")


	@server.command()
	async def start(self, ctx):
		await start_remote.start(ctx)

	@server.command()
	async def check(self, ctx):
		await ctx.response.defer()
		msg = await ctx.interaction.send("hello")
		if check_server_status() == 0:
			await msg.edit(f"checking: Minecraft Server is accessable ")
		else:
			await msg.edit(f"checking: Minecraft Server is down! Is proxy down? ")
			await msg.edit("-# This instance of kurisu environment is running locally.")



def setup(bot):
	bot.add_cog(Minecraft(bot))