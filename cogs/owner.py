import discord 
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.group(invoke_without_command = True, aliases = ('ad',))
    async def admin(self, ctx):
        """ Used to change the settings of the bot. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Add\n2.Remove')
        
        return await ctx.send(embed = e)

    @commands.is_owner()
    @admin.command(aliases = ('a',))
    async def add(self, ctx, user: discord.Member = None):
        """ Add a user as a editor. """
        if not user:
            return await ctx.send('Please provide a user.')
        
        data = self.bot.mongo.mongo.settings.find_one({'_id': 0})
        if data:
            if user.id in data['editors']:
                return await ctx.send(f'<@{user.id}> is already a editor.')
            else:
                data['editors'].insert(user.id)
                self.bot.mongo.mongo.settings.update_one({'_id': 0}, {'$set': data}, upsert = True)
        else:
            data = {'_id': 0, 'editors': [user.id]}
            self.bot.mongo.mongo.settings.insert_one(data)
        return await ctx.send(f'<@{user.id}> is added to editor list.')

    @commands.is_owner()
    @admin.command(aliases = ('r',))
    async def remove(self, ctx, user: discord.Member = None):
        """ Remove a user from editor list. """
        if not user:
            return await ctx.send('Please provide a user.')

        data = self.bot.mongo.mongo.settings.find_one({'_id': 0})
        if data:
            if user.id not in data['editors']:
                return await ctx.send(f'<@{user.id}> is not a editor.')
            else:
                data['editors'].remove(user.id)
                self.bot.mongo.mongo.settings.update_one({'_id': 0}, {'$set': data}, upsert = True)
                return await ctx.send(f'<@{user.id}> is removed from the editor list.')
    
def setup(bot):
    bot.add_cog(Owner(bot))