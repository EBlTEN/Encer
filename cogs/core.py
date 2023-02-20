from logging import getLogger
import time

import discord
from discord.ext import commands
from discord import app_commands


logger = getLogger("Encer").getChild("sub")

# UNIX時間を記録
start_time = int(time.time())


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("%s is loaded", __name__)

    @app_commands.command()
    async def monitor(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"`{self.bot.latency*1000:.0f}`ms\n稼働開始:<t:{start_time}:R>")


async def setup(bot):
    await bot.add_cog(Core(bot))
