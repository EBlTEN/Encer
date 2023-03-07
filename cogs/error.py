import json
from logging import getLogger
import traceback

import discord
from discord.ext import commands
from discord.app_commands import AppCommandError

import modules


logger = getLogger(f"discord.{__name__}")


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
        embed = modules.embed(
            title="Error", description=f"{type(error)}\n{traceback.format_exception_only(type(error), error)}")
        embed.set_author(name=interaction.command.name)
        await interaction.response.send_message(embed=embed)

        logger.error("%s (ID: %s)", error, interaction.id)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")


async def setup(bot):
    await bot.add_cog(Error(bot))
