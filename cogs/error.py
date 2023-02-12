import json
from logging import getLogger
import traceback

import discord
from discord.ext import commands
from discord.app_commands import AppCommandError


logger = getLogger("Encer").getChild("sub")


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = tree.__class__.on_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: AppCommandError):
        #        with open("./error_message.json") as msg:
        #            erra = msg["voice"][error]
        embed = discord.Embed(title=type(error), description=traceback.format_exception_only(type(error), error),
                              color=discord.Colour.from_rgb(255, 0, 0))
        embed.set_author(name=interaction.command.name)
        embed.set_footer(
            text=f"Encer.error.message")
        await interaction.response.send_message(embed=embed)

        logger.error("%s (ID: %s)", error, interaction.id)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("%s is loaded", __name__)


async def setup(bot):
    await bot.add_cog(Error(bot))
