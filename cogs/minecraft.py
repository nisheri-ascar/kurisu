import discord
from discord.ext import commands

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
		await ctx.respond("success!")



def setup(bot):
	bot.add_cog(Minecraft(bot))