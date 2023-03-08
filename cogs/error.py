import traceback
from logging import getLogger

import discord
from discord.app_commands import AppCommandError
from discord.ext import commands

import modules

logger = getLogger(f"discord.{__name__}")


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")

    # エラーハンドリングがしにくくなるので一旦削除


async def setup(bot):
    await bot.add_cog(Error(bot))
