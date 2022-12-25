import discord
from discord.ext import commands
from discord import app_commands

Root_guild = discord.Object(681015774885838896)


class Cog_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog_manager is loaded")

    @app_commands.command(name="load", description="test")
    async def load(self, ctx: discord.Interaction):
        ctx.respond("pong")


async def setup(bot):
    await bot.add_cog(Cog_manager(bot), guild=Root_guild)
