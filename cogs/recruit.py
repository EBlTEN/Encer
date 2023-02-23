from logging import getLogger
import re


import discord
from discord.ext import commands
from discord import app_commands


logger = getLogger("Encer").getChild("sub")


class Recruit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("%s is loaded", __name__)

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
        # 設定していたcustom_idを参照
        custom_id = interaction.data["custom_id"]
        # buttonの押されたmessageのidを取得
        message = await interaction.channel.fetch_message(interaction.message.id)
        # messageのidからembedのオブジェクトを生成
        embed = message.embeds[0]
        # embedのvalueを\nを区切り文字としてlistに書き出す
        member_list = embed.fields[0].value.split("\n")
        # 正規表現で人数を取得
        member_count = int(re.sub(r"\D+", "", embed.fields[0].name))

        if custom_id == "join":
            # すでにlistの中にidがあったらエラーを返す
            if f"<@{interaction.user.id}>" in member_list:
                await interaction.response.send_message(
                    "すでに参加しています。", ephemeral=True)
            else:
                # embedのvalueにuser idを,member_countを-1して追記
                member_count -= 1
                embed.set_field_at(
                    0, name=f"あと`{member_count}`人", value=f"{message.embeds[0].fields[0].value}\n<@{interaction.user.id}>")
                await interaction.response.send_message("参加しました。", ephemeral=True)
        elif custom_id == "leave":
            # 要素の削除
            try:
                member_list.remove(f'<@{interaction.user.id}>')
            # listにidが無い場合はValueErrorが出るのでキャッチしてmessage
            except ValueError:
                await interaction.response.send_message("参加していません。", ephemeral=True)
            # 正常に削除できた場合の処理
            else:
                # listをembedのfieldへ上書き,member_countを+1
                member_count += 1
                embed.set_field_at(
                    0, name=f"あと`{member_count}`人", value="\n".join(member_list))
                # messageの送信
                await interaction.response.send_message("辞退しました。", ephemeral=True)

        # embedをedit
        if member_count <= 0:
            # member_countが0以下になったらボタンを消して締める
            await message.edit(embed=embed, view=None)
        else:
            await message.edit(embed=embed)

    @app_commands.command(name="rect", description="メンバー募集メッセージを作成する")
    @app_commands.commands.describe(title="タイトル", limit="最大人数")
    async def rect(self, interaction: discord.Interaction, title: str, limit: int):
        # buttonの作成
        join = discord.ui.Button(
            label="参加", style=discord.ButtonStyle.primary, custom_id="join")
        leave = discord.ui.Button(
            label="辞退", style=discord.ButtonStyle.primary, custom_id="leave")
        view = discord.ui.View()
        view.add_item(join)  # ここらへんもうちょっとスマートにしたい
        view.add_item(leave)
        # embedの作成
        embed = discord.Embed(title="募集", description=title)
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.avatar.url
                         )
        embed.add_field(name=f"あと`{limit}`人",
                        value=f"<@{interaction.user.id}>")
        embed.set_footer(text=f"Encer.commands.Recruit")
        await interaction.response.send_message(embed=embed, view=view)
        # print(interaction.channel.last_message_id)


async def setup(bot):
    await bot.add_cog(Recruit(bot))
