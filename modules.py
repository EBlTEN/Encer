import inspect
import logging

import discord

owner_id = [501340685757186059, 585858021415190550]


# botの開発者かどうか判定する
def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id in owner_id


def embed(*, title,  description=None, url=None, color_code: str = "#32cd32"):
    func_name = inspect.stack()[1].function  # 呼び出し元の関数名を取得
    # statusに合わせてembedの色を変える
    color_list = {
        "Info": "#4682b4",
        "Warn": "#ff7f50",
        "Error": "#b22222"
    }

    try:
        color = color_list[title]
    except KeyError:  # 不明なstatusはカラーコードを参照して送信
        return discord.Embed(title=title, description=description, colour=discord.Colour.from_str(color_code), url=url,).set_footer(text=f"Encer.{func_name}")

    return discord.Embed(title=title, description=description, colour=discord.Colour.from_str(color), url=url,).set_footer(text=f"Encer.{func_name}.{title}")
