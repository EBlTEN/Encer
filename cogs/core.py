from logging import getLogger
import time

import discord
from discord.ext import commands
from discord import app_commands


logger = getLogger("Encer").getChild("sub")

# UNIX時間を記録
start_time = int(time.time())


class Core(commands.GroupCog, group_name="encer"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("%s is loaded", __name__)
        await self.bot.change_presence(activity=discord.Game(name="/encer help"))

    @app_commands.command(description="このbotについて表示する")
    async def about(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://github.com/EBlTEN/Encer")

    @app_commands.command(description="このbotの状態を表示する")
    async def monitor(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"`{self.bot.latency*1000:.0f}`ms\n稼働開始:<t:{start_time}:R>")

    @app_commands.command(description="helpを表示する")
    async def help(self, interaction: discord.Interaction):
        def get_group_command_help_text(group: discord.app_commands.Group):
            cmd_name = ""
            group_cmd_count = 0
            group_name = get_command_help_text(group)  # グループ名を取得
            for cmd in group.walk_commands():  # グループ内のコマンドを取得
                # cmd_nameに追記していく
                cmd_help_text = get_command_help_text(cmd)
                cmd_name += f"`{cmd_help_text[0]}`:{cmd_help_text[1]}\n"
                group_cmd_count += 1
            return (group_name[0], cmd_name, group_cmd_count)

        def get_command_help_text(cmd: discord.app_commands.Group | discord.app_commands.Command):
            cmd_name = cmd.name
            cmd_description = ""
            if cmd.description != "…":  # 説明がついている場合は説明も取得
                cmd_description = cmd.description
            return (cmd_name, cmd_description)

        cmd_count = 0
        group_count = 0

        embed = discord.Embed(title="Encer Help")
        embed.set_footer(text=f"Encer.commands.Core")
        commands = self.bot.tree.get_commands()
        for cmd in commands:
            # インスタンスを取得して条件分岐
            if isinstance(cmd, discord.app_commands.Group):  # グループの場合
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
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Core(bot))
