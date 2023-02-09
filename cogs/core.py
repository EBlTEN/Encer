from logging import getLogger

import discord
from discord.ext import commands
from discord import app_commands

from modules import Optime


logger = getLogger("Encer").getChild("sub")

ts = Optime()


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("%s is loaded", __name__)

    @app_commands.command()
    async def monitor(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"`{self.bot.latency*1000:.0f}`ms\n稼働開始 {ts.optime()}")


async def setup(bot):
    await bot.add_cog(Core(bot))
