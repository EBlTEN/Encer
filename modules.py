import datetime
import time

import discord


class Optime():
    def __init__(self):
        self.start = int(time.time())

    def optime(self):
        return (f"<t:{self.start}:R>")


class Embed_info():

    def success_embed(msg):
        embed = discord.Embed(title="Success", description=msg,
                              color=discord.Colour.from_rgb(0, 255, 0))
        return embed

    def error_embed(err):
        embed = discord.Embed(title="Error", description=err,
                              color=discord.Colour.from_rgb(255, 0, 0))
        return embed
