import os
import time
from logging import getLogger, config
import json

import discord
from discord import app_commands
from discord.ext import commands

# loggerの設定ファイルを読み込み
with open("./log_config.json", "r")as f:
    log_config = json.load(f)

config.dictConfig(log_config)

# loggerインスタンス
logger = getLogger(__name__)

# デバッグ用のサーバーIDEA
Root_guild = discord.Object(681015774885838896)


class Encer(commands.Bot):
    async def setup_hook(self):
        # ここでcogを読み込む
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                except Exception as err:
                    logger.error(err)
        # slashcommandを登録
        self.tree.copy_global_to(guild=Root_guild)
        await self.tree.sync(guild=Root_guild)

        # インテントの定義
intents = discord.Intents.default()
bot = Encer(command_prefix="League_of_legends",
            intents=intents, help_command=None)


# ログインしたらコンソールにメッセージを表示
@bot.event
async def on_ready():
    logger.info(f"Logged in to {bot.user}(ID: {bot.user.id})")


# cogの管理コマンド群
@bot.tree.command(name="cog", description="cogsフォルダ内に存在するcogの管理をする。")
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
    # 各オプションに対応した処理をする。
    try:
        if mode == "load":
            await bot.load_extension(f"cogs.{cog}")
        elif mode == "reload":
            await bot.reload_extension(f"cogs.{cog}")
        elif mode == "unload":
            await bot.unload_extension(f"cogs.{cog}")
    # エラーハンドリング
    except (
        discord.ext.commands.errors.ExtensionNotFound,
        discord.ext.commands.errors.ExtensionNotLoaded,
        discord.app_commands.errors.CommandInvokeError
    ) as err:
        await interaction.response.send_message(err)
        logger.error(err)
    # 正常に完了したらメッセージを送信
    else:
        await interaction.response.send_message(f"{cog} has been {mode}ed.")
        logger.info(f"{cog} has been {mode}ed.")

# Bot本体の起動
TOKEN = os.environ['DISCORD_TOKEN']
bot.run(TOKEN)
