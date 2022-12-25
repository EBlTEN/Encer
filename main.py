import os
import discord
from discord import app_commands
from discord.ext import commands

Root_guild = discord.Object(681015774885838896)


class Encer(commands.Bot):
    async def setup_hook(self):
        self.tree.copy_global_to(guild=Root_guild)
        await self.tree.sync(guild=Root_guild)
        # ここでcogを読み込む
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")


# インテントの定義
intents = discord.Intents.default()
bot = Encer(command_prefix="League_of_legends",
            intents=intents, help_command=None)

# ログインしたらコンソールにメッセージを表示


@bot.event
async def on_ready():
    print(f"Welcome to {bot.user}'s console")

# テストコマンド


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{bot.latency*1000:.0f}ms")

# ここから下はコピーしない
# Bot本体の起動
bot.run("ODU2NDUzNTU0NjQyMjIzMTA1.YNBQhw.Wt8jxvwjRTNNnt5CGXqR0vE8_Zg")
