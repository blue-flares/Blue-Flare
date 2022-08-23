import discord

from datetime import datetime

def data_update(ctx, title, color):
    e = discord.Embed()
    e.title = title
    e.color = color
    e.timestamp = datetime.now()
    e.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.display_avatar)

    return e

def error_embed(ctx, description):
    e = discord.Embed(
            title = 'Error',
            description = description,
            color = discord.Color.red(),
            timestamp = datetime.now()
        )
    e.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.display_avatar)
    
    return e