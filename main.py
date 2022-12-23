import discord
from discord.ext import commands

import config 

import aiohttp
import datetime
import contextlib
import asyncio

cog_extension = [
    'jishaku',
    'cogs.mongo',
    'cogs.donation',
    'cogs.error',
    'cogs.misc',
    'cogs.owner',
    'cogs.username', 
    'cogs.battle', 
    'cogs.chat',
    'cogs.wtp',
    'cogs.leaderboard'
]

class BlueFlare(commands.Bot):
    def __init__(self):
        super().__init__(
          command_prefix = commands.when_mentioned_or(
            "bf",
            "BF",
            "Bf",
            "bF"
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
        print(f"Logged in {self.user.name} (ID {self.user.id})\nVersion {discord.__version__}")

    async def setup_hook(self):
        for cog in cog_extension:
            await self.load_extension(cog)
            """
            try:
                await self.load_extension(cog)
            except:
                print(f'Failed to load extension: {cog}')"""

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(config.WEBHOOK, session=session)
            await webhook.send('Blue Flare Online.', username = 'Blue Flare')

    async def on_message(self, message):
      if message.author.bot:
        return 
      if message.content == f'<@{self.user.id}>':
        embed = discord.Embed(
          title = 'Blue Flare Bot',
          description = f'Prefixes : <@{self.user.id}>, bf\n Developer : <@724447396066754643>',
          color = discord.Color.blue(),
          timestamp = discord.utils.utcnow()
        )
        await message.channel.send(embed = embed)
      await self.process_commands(message)
    
    async def on_message_edit(self, before, after):
      if after.author.id in self.owner_ids:
        await self.process_commands(after)
      else:
        return
    
    async def start(self):
        await super().start(config.TOKEN, reconnect = True)

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    @property
    def mongo(self):
        return self.get_cog('Mongo')

bot = BlueFlare()

class HelpEmbed(discord.Embed):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = discord.Color.blurple()


class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(  
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.user),
                "aliases": ['commands']
            }
        )

    async def send(self, **kwargs):
        """a shortcut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.display_avatar)
        usable = 0

        for cog, commands in mapping.items():  
            if filtered_commands := await self.filter_commands(commands):
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:   
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No"
                    description = "Commands with no category"

                embed.add_field(name=f"{name} Category [{amount_commands}]", value=description)

        embed.description = f"{len(bot.commands)} commands | {usable} usable"

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        signature = self.get_command_signature(
            command)  
        embed = HelpEmbed(title=signature, description=command.help or "No help found...")

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
       
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"

        embed.add_field(name="Usable", value=can_run)

        if command._buckets and (
        cooldown := command._buckets._cooldown):  
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands):  
        embed = HelpEmbed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")

        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

bot.help_command = MyHelp()


asyncio.run(bot.start())