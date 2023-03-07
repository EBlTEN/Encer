from logging import getLogger
import random

import discord
from discord.ext import commands
from discord import app_commands

import modules

logger = getLogger(f"discord.{__name__}")


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")

    @app_commands.command(description="VCのメンバーを指定されたチーム数に分割する")
    @app_commands.describe(teams="用意するチーム数(初期値:2)",
                           exclusion="チーム分けから除外するメンバーのID")
    async def team(self, interaction: discord.Interaction, teams: int = 2, exclusion: str = "None"):
        exclusion_names = []  # 必要な変数の定義

        # VCのメンバーをlistで取得
        try:
            vc_members = interaction.user.voice.channel.members
        except AttributeError:
            embed = modules.embed(
                title="Error", description="VCのidを取得できませんでした。")
            embed.set_author(name=interaction.command.name)
            await interaction.response.send_message(embed=embed)
            return

        # 取得した要素の名前とidを抽出してdictにする
        vc_dict = {i.id: i.name for i in vc_members}

        # exclusion引数に入っているIDがある場合の処理
        if exclusion != "None":
            logger.debug("Variable exclusion is found")
            exclusion_list = exclusion.split(",")  # ","を区切り文字としてidをlistに入れる
            # 作成したlistを元にメンバーリストから値を削除
            for exclusion_id in exclusion_list:
                # dictにidで検索かけて除外者リストを作成
                exclusion_names.append(vc_dict[int(exclusion_id)])
                del vc_dict[int(exclusion_id)]

        member_list = [f"<@{i}>" for i in list(vc_dict.keys())]
        random.shuffle(member_list)  # listをshuffle

        # embedを作成
        embed = discord.Embed(
            title="Teams", description=f"チーム数:{teams}\n除外:{', '.join(exclusion_names)}\n")
        embed.set_footer(text=f"Encer.commands.Voice")

        # n等分
        for i in range(teams):
            embed.add_field(name=f"Team{i+1}",
                            value="\n".join(member_list[i:len(member_list):teams]))

        await interaction.response.send_message(embed=embed)  # embedを送信


async def setup(bot):
    await bot.add_cog(Voice(bot))
