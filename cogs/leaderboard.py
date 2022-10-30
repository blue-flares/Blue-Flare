import discord
from discord.ext import commands

from utility.leaderboard import LeaderBoardHelper

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lb = LeaderBoardHelper()

    @commands.command()
    async def lb(self, ctx):
        e = self.lb.donation(ctx)

        await ctx.send(embed = e)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))