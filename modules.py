import discord
import inspect

owner_id = [501340685757186059, 585858021415190550]


def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id in owner_id


def embed(*, title, status, description=None, url=None):
    func_name = inspect.stack()[1].function  # 呼び出し元の関数名を取得
    # statusに合わせてembedの色を変える
    color_list = {
        "info": discord.Colour.from_rgb(0, 0, 255),
        "success": discord.Colour.from_rgb(0, 255, 0),
        "warn": discord.Colour.from_rgb(255, 165, 0),
        "error": discord.Colour.from_rgb(255, 0, 0)
    }

    try:
        color = color_list[status]
    except KeyError:  # 不明なstatusは黒色へ置換
        color = discord.Colour.from_rgb(0, 0, 0)
    return discord.Embed(title=title, description=description, colour=color, url=url,).set_footer(text=f"Encer.{func_name}.{status}",)
