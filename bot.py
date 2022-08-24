import discord
from discord.ext import commands

import config

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
          command_prefix = commands.when_mentioned_or(
            "!"
          ), 
          intents = discord.Intents.all(), 
          strip_after_prefix = True,
          owner_ids = {
            724447396066754643
          }, 
          case_insensitive = False, 
          self_bot = False,
          allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        )
        
    async def on_ready(self):
        print(f"Logged in as {self.user.name} with id {self.user.id}\nVersion {discord.__version__}")

    async def on_message(self, message):
      if message.author.bot:
        return 
      if message.content == f'<@{self.user.id}>':
        embed = discord.Embed(
          title = 'Blue Flare Bot',
          description = f'Prefixes : <@{self.user.id}>, bf\n Developer : <@724447396066754643>',
          color = discord.Color.random()
        )
        await message.channel.send(embed = embed)
      await bot.process_commands(message)

    @property
    def mongo(self):
        return self.get_cog('Mongo')

bot = Bot() 

cog_extension = [
  'cogs.mongo',
  'cogs.donation',
  'cogs.error',
  'cogs.misc',
  'cogs.owner',
  'cogs.username'
]

for cog in cog_extension:
  bot.load_extension(cog)

bot.run(config.TOKEN)