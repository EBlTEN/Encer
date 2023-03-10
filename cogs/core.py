import time
from logging import getLogger

import discord
from discord import app_commands, ui
from discord.ext import commands

import modules

logger = getLogger(f"discord.{__name__}")
start_time = int(time.time())  # UNIX時間を記録


class MessageForm(ui.Modal, title="お問い合わせ"):
    form = ui.TextInput(
        label="意見、要望など", style=discord.TextStyle.paragraph, custom_id="report")

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(1079832762766344324)
        embed = modules.embed(title="report",
                              description=interaction.data["components"][0]["components"][0]["value"])  # 送信されたメッセージの内容を取得
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.avatar.url
                         )
        embed.set_footer(text=f"Encer.commands.Core.report")
        await channel.send(embed=embed)  # 開発サーバーに送信
        # ユーザーに返信
        embed = modules.embed(title="Info", description="メッセージを送信しました。")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Core(commands.GroupCog, group_name="encer"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")
        await self.bot.change_presence(activity=discord.Game(name="/encer help"))

    @app_commands.command(description="このbotについて表示する")
    async def about(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://github.com/EBlTEN/Encer", ephemeral=True)

    @app_commands.command(description="このbotの状態を表示する")
    async def monitor(self, interaction: discord.Interaction):
        embed = modules.embed(
            title="Info", description=f"`{self.bot.latency*1000:.0f}`ms\n稼働開始:<t:{start_time}:R>")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="開発サーバーにメッセージを送信する")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MessageForm(self.bot))

    @app_commands.command(description="helpを表示する")
    async def help(self, interaction: discord.Interaction):
        def get_group_command_help_text(group: app_commands.Group):
            cmd_name = ""
            group_cmd_count = 0
            group_name = get_command_help_text(group)  # グループ名を取得
            for cmd in group.walk_commands():  # グループ内のコマンドを取得
                # cmd_nameに追記していく
                cmd_help_text = get_command_help_text(cmd)
                cmd_name += f"`{cmd_help_text[0]}`:{cmd_help_text[1]}\n"
                group_cmd_count += 1
            return (group_name[0], cmd_name, group_cmd_count)

        def get_command_help_text(cmd: app_commands.Group | app_commands.Command):
            cmd_name = cmd.name
            cmd_description = ""
            if cmd.description != "…":  # 説明がついている場合は説明も取得
                cmd_description = cmd.description
            return (cmd_name, cmd_description)

        cmd_count = 0
        group_count = 0

        embed = modules.embed(title="Encer Help",
                              url="https://github.com/EBlTEN/Encer/wiki")
        commands = self.bot.tree.get_commands()
        for cmd in commands:
            # インスタンスを取得して条件分岐
            if isinstance(cmd, app_commands.Group):  # グループの場合
                group_count += 1
                cmd_info = get_group_command_help_text(cmd)
                embed.add_field(
                    name=cmd_info[0], value=f"{cmd_info[1]}", inline=False)
                cmd_count += cmd_info[2]
            else:  # 単体の場合
                cmd_count += 1
                cmd_info = get_command_help_text(cmd)
                embed.add_field(name=cmd_info[0],
                                value=cmd_info[1], inline=True)

        embed.description = f"コマンド数:`{cmd_count}`\nグループ数:`{group_count}`"
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Core(bot))
