import discord
from discord.ext import commands

import asyncio

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        """ Show the profile of a user. """
        user = user or ctx.author
        data = self.bot.mongo.fetch(user.id)

        if not data:
            return await ctx.send(f'<@{user.id}> has no entry in the database.')

        e = discord.Embed(
            title = f'{user.name}\'s profile',
            description = f"Username: {data['username']}\nDonation: {data['donation']}",
            timestamp = discord.utils.utcnow(),
            color = discord.Color.blue()
        )
        e.add_field(name = 'Battle', value = f"Win: {data['win']}\nLose: {data['lose']}\nDraw: {data['draw']}")
        e.set_thumbnail(user.display_avatar)

        await ctx.send(embed = e)

    @commands.command(aliases = ('elist', 'el', 'editorlist'))
    async def editor_list(self, ctx):
        """ Show all the editors (who can change database.) """
        data = self.bot.mongo.mongo.settings.find_one({'_id': 0})['editors']
        mentions = '\n'.join([f'<@{a}>' for a in data])

        e = discord.Embed(
            title = 'Editors',
            description = f'{mentions}',
            color = discord.Color.blue(),
            timestamp = discord.Color.blue
        )
        e.set_footer(text = 'Ask them to changed any incorrect data.')

        await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(Misc(bot))
