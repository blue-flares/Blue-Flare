from discord.ext import commands

class NotEditor(commands.CheckFailure):
    pass

def is_editor():
    def predicate(ctx):
        data = ctx.bot.mongo.mongo.settings.find_one({'_id': 0})['editors']
        if ctx.author.id not in data:
            raise NotEditor('You are not a editor.')
            return False
        return True
    return commands.check(predicate)