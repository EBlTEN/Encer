import json
from logging import getLogger, config
import os
import time

import discord
from discord.ext import commands
from discord import app_commands

import checker


# loggerの設定ファイルを読み込み
with open("./log_config.json", "r")as f:
    log_config = json.load(f)

config.dictConfig(log_config)

# loggerインスタンス
logger = getLogger("Encer")

# デバッグ用のサーバーID
Root_guild = discord.Object(681015774885838896)

# cogのリストを生成
cog_list = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cog_list.append(filename[:-3])
print(cog_list)


class Encer(commands.Bot):
    async def setup_hook(self):
        # ここでcogを読み込む
        try:
            for cog in cog_list:
                await bot.load_extension(f"cogs.{cog}")
        except Exception as err:
            logger.error(err)

        # slash commandを登録
        # self.tree.copy_global_to(guild=Root_guild)
        await self.tree.sync()


        # intentsの定義
intents = discord.Intents.all()
bot = Encer(command_prefix="League_of_legends",
            intents=intents, help_command=None)


@bot.event
async def on_ready():
    # ログインしたらコンソールにメッセージを表示
    logger.info("Logged in to %s (ID: %s)", bot.user, bot.user.id)


# cogの管理コマンド
@bot.tree.command(name="cog", description="cogsフォルダ内に存在するcogの管理をする。")
@discord.app_commands.check(checker.is_owner)
# モードの入力補完設定
@discord.app_commands.choices(
    mode=[
        discord.app_commands.Choice(name="load", value="load"),
        discord.app_commands.Choice(name="reload", value="reload"),
        discord.app_commands.Choice(name="unload", value="unload")
    ]
)
@discord.app_commands.describe(cog="cogsフォルダ内のcogファイル")
async def cog(interaction: discord.Interaction, mode: str, cog: str):
    # 各モードの処理
    if mode == "load":
        await bot.load_extension(f"cogs.{cog}")
    elif mode == "reload":
        await bot.reload_extension(f"cogs.{cog}")
    elif mode == "unload":
        await bot.unload_extension(f"cogs.{cog}")

    embed = discord.Embed(title="Success", description=f"{cog} has been {mode}ed.",
                          color=discord.Colour.from_rgb(0, 255, 0))
    await interaction.response.send_message(embed=embed, ephemeral=True)
    logger.info("%s has been %sed.", cog, mode)


# Bot本体の起動
TOKEN = os.environ['DISCORD_TOKEN']
bot.run(TOKEN)
