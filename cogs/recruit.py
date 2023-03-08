import asyncio
import re
from logging import getLogger

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput, View

import modules

logger = getLogger(f"discord.{__name__}")

# buttonの作成
join = discord.ui.Button(
    label="参加", style=discord.ButtonStyle.primary, custom_id="join")
leave = discord.ui.Button(
    label="辞退", style=discord.ButtonStyle.primary, custom_id="leave")
delete = discord.ui.Button(
    label="削除(作成者のみ)", style=discord.ButtonStyle.danger, custom_id="delete")


class Recruit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")

    # buttonが押されたときの処理
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # buttonが押されたか判定
        try:
            if interaction.data['component_type'] == 2:
                await Recruit.on_button_click(interaction)
        # それ以外は無視
        except KeyError:
            pass

    async def on_button_click(interaction: discord.Interaction):

        custom_id = interaction.data["custom_id"]  # 設定していたcustom_idを参照
        # buttonの押されたmessageのidを取得
        message = await interaction.channel.fetch_message(interaction.message.id)
        embed = message.embeds[0]  # messageのidからembedのオブジェクトを生成
        member_list = embed.fields[0].value.split(
            "\n")  # embedのvalueを\nを区切り文字としてlistに書き出す
        member_count = int(
            re.sub(r"\D+", "", embed.fields[0].name))  # 正規表現で人数を取得

        if custom_id == "join":  # 参加
            # すでにlistの中にidがあったらエラーを返す
            if f"<@{interaction.user.id}>" in member_list:
                output_embed = modules.embed(
                    title="Warn", description="すでに参加しています。")
                await interaction.response.send_message(embed=output_embed, ephemeral=True)
            else:
                # embedのvalueにuser idを,member_countを-1して追記
                member_count -= 1
                embed.set_field_at(
                    0, name=f"あと`{member_count}`人", value=f"{message.embeds[0].fields[0].value}\n<@{interaction.user.id}>")
                output_embed = modules.embed(
                    title="Info", description="参加しました。")
                await interaction.response.send_message(embed=output_embed, ephemeral=True)
        elif custom_id == "leave":  # 辞退
            # 要素の削除
            try:
                member_list.remove(f'<@{interaction.user.id}>')
            # listにidが無い場合はValueErrorが出るのでキャッチしてmessage
            except ValueError:
                output_embed = modules.embed(
                    title="Warn", description="参加していません。")
                await interaction.response.send_message(embed=output_embed, ephemeral=True)

            else:  # 正常に削除できた場合の処理
                # listをembedのfieldへ上書き,member_countを+1
                member_count += 1
                embed.set_field_at(
                    0, name=f"あと`{member_count}`人", value="\n".join(member_list))

                output_embed = modules.embed(
                    title="Info", description="辞退しました。")
                await interaction.response.send_message(embed=output_embed, ephemeral=True)

        elif custom_id == "delete":  # 削除
            if str(interaction.user) == embed.author.name:
                embed = modules.embed(title="募集", description="削除されました")
                await message.edit(embed=embed, view=None, delete_after=5)
            else:
                output_embed = modules.embed(
                    title="Error", description="削除に失敗しました\n削除はコマンドの実行者のみ行えます。")
                await interaction.response.send_message(embed=output_embed, ephemeral=True)

        if member_count <= 0:
            # member_countが0以下になったらボタンを変更して締める
            view = View()
            view.add_item(leave)
            view.add_item(delete)
            await message.edit(embed=embed, view=view)
        else:
            view = View()
            view.add_item(join)  # ここらへんもうちょっとスマートにしたい
            view.add_item(leave)
            view.add_item(delete)
            await message.edit(embed=embed, view=view)

    @app_commands.command(name="rect", description="メンバー募集メッセージを作成する")
    @app_commands.commands.describe(title="タイトル", limit="最大人数")
    async def rect(self, interaction: discord.Interaction, title: str, limit: int):
        await interaction.response.send_message(
            f"{title}\nあと{limit}人")  # 通常メッセージでメンションを飛ばす
        message = await interaction.original_response()

        view = View()
        view.add_item(join)  # ここらへんもうちょっとスマートにしたい
        view.add_item(leave)
        view.add_item(delete)
        # embedの作成
        embed = modules.embed(title="募集", description=title)
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.avatar.url
                         )
        embed.add_field(name=f"あと`{limit}`人",
                        value=f"<@{interaction.user.id}>")
        await asyncio.sleep(1)
        await message.edit(content=None, embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Recruit(bot))
