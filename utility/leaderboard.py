import discord

class LeaderBoardHelper():
    def __init__(self):
        pass

    def chat(self, ctx):
        data = ctx.bot.mongo.col.find().sort('chat', -1).limit(10)

        e = discord.Embed(
            title = 'Chat LeaderBoard',
            color = discord.Color.blue(),
            timestamp = discord.utils.utcnow()
        )
        user, value = [], []
        count = 0

        for a in data:
            count += 1
            user.append(a['_id'])
            value.append(a['chat'])

        e.add_field(name = 'Place', value = '\n'.join(range(1,len(value)+1)), inline = True)
        e.add_field(name = 'Member', value = '\n'.join([f'<@{a}>' for a in user]), inline = True)
        e.add_field(name = 'Chat Winner', value = '\n'.join(value), inline = True)
        e.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.display_avatar)

        return e

    def battle(self, ctx):
        data = ctx.bot.mongo.col.find().sort('win', -1).limit(10)

        e = discord.Embed(
            title = 'Chat LeaderBoard',
            color = discord.Color.blue(),
            timestamp = discord.utils.utcnow()
        )
        user, value = [], []
        count = 0

        for a in data:
            count += 1
            user.append(a['_id'])
            value.append(str(a['win']))

        e.add_field(name = 'Place', value = '\n'.join([str(a) for a in range(1,len(value)+1)]), inline = True)
        e.add_field(name = 'Member', value = '\n'.join([f'<@{a}>' for a in user]), inline = True)
        e.add_field(name = 'Battle Won', value = '\n'.join(value), inline = True)
        e.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.display_avatar)

        return e

    def donation(self, ctx):
        data = ctx.bot.mongo.col.find().sort('donation', -1).limit(10)
        

        e = discord.Embed(
            title = 'Chat LeaderBoard',
            color = discord.Color.blue(),
            timestamp = discord.utils.utcnow()
        )
        user, value = [], []
        count = 0

        for a in data:
            count += 1
            user.append(a['_id'])
            value.append(str(a['donation']))

        e.add_field(name = 'Place', value = '\n'.join([str(a) for a in range(1,len(value)+1)]), inline = True)
        e.add_field(name = 'Member', value = '\n'.join([f'<@{a}>' for a in user]), inline = True)
        e.add_field(name = 'Donation(in m)', value = '\n'.join(value), inline = True)
        e.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.display_avatar)

        return e