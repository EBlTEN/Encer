import discord

owner_id = [501340685757186059, 585858021415190550]


def is_owner(interaction: discord.Integration) -> bool:
    return interaction.user.id in owner_id
