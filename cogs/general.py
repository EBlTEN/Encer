import discord
from discord.ext import commands
from discord import app_commands

import sys

Root_guild = discord.Object(681015774885838896)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog_manager is loaded")

    @app_commands.command()
    async def stuts(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"`{self.bot.latency*1000:.0f}`{}")


async def setup(bot):
    await bot.add_cog(General(bot), guild=Root_guild)
