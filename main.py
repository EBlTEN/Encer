import logging
import logging.handlers
import os

import discord
from discord import app_commands
from discord.ext import commands

import modules

# loggerインスタンスの生成
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

# フォーマット
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")

# ファイルに出力するlogの設定
file_handler = logging.handlers.RotatingFileHandler(
    filename="Encer.log",
    encoding="utf-8",
    maxBytes=8 * 1024*1024,
    backupCount=5
)
file_handler.setFormatter(formatter)

# コンソールに出力するlogの設定
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# loggerにhandlerを追加
logger.addHandler(console_handler)
logger.addHandler(file_handler)

Root_guild = discord.Object(681015774885838896)  # デバッグ用のサーバーID
cog_list = []  # cogのリストを生成

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        cog_list.append(filename[:-3])


class Encer(commands.Bot):
    async def setup_hook(self):
        # ここでcogを読み込む
        try:
            for cog in cog_list:
                await bot.load_extension(f"cogs.{cog}")
        except Exception as err:
            logger.error(err)

        await self.tree.sync()  # slash commandを登録


intents = discord.Intents.all()  # intentsの定義
bot = Encer(command_prefix="League_of_legends",
            intents=intents, help_command=None)


@bot.event
async def on_ready():
    logger.info("Logged in to %s (ID: %s)", bot.user,
                bot.user.id)  # ログインしたらコンソールにメッセージを表示


# logファイルの送信コマンド
@bot.tree.command(description="logファイルを送信する")
@app_commands.check(modules.is_owner)
async def log(interaction: discord.Interaction, number: int = None):
    # バックアップファイルを指定したときの処理
    if number != None:
        file_name = f"Encer.log.{number}"
    else:
        file_name = "Encer.log"

    try:
        log_file = discord.File(f"./{file_name}", filename=file_name)
        embed = modules.embed(
            title="Info", description="logファイルの送信に成功しました。")
    except FileNotFoundError:  # ファイルが見つからなかったらエラー
        embed = modules.embed(
            title="Error", description=f"{file_name}は存在しません。")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    await interaction.response.send_message(file=log_file, ephemeral=True)


# cogの管理コマンド
@bot.tree.command(description="cogsフォルダ内に存在するcogの管理をする。")
@app_commands.check(modules.is_owner)
# モードの入力補完設定
@app_commands.choices(
    mode=[
        app_commands.Choice(name="load", value="load"),
        app_commands.Choice(name="reload", value="reload"),
        app_commands.Choice(name="unload", value="unload")
    ]
)
@app_commands.describe(cog="cogsフォルダ内のcogファイル")
async def cog(interaction: discord.Interaction, mode: str, cog: str):
    # 各モードの処理
    if mode == "load":
        await bot.load_extension(f"cogs.{cog}")
    elif mode == "reload":
        await bot.reload_extension(f"cogs.{cog}")
    elif mode == "unload":
        await bot.unload_extension(f"cogs.{cog}")

    embed = modules.embed(
        title="Success", description=f"{cog} has been {mode}ed.")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    logger.info("%s has been %sed.", cog, mode)

TOKEN = os.environ['DISCORD_TOKEN']
bot.run(TOKEN, log_handler=None)  # Bot本体の起動
