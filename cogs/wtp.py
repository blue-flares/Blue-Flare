import discord
from discord.ext import commands
import aiohttp
import asyncio
import random

class WTP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_data(self, poke_id):
        session = aiohttp.ClientSession()
        async with session.get(f'https://pokeapi.co/api/v2/pokemon-species/{poke_id}') as data:
            return await data.json()
    
    @commands.command()
    async def wtp(self, ctx):
        poke_id = random.randint(1,905)
        h_img = f'https://raw.githubusercontent.com/Hemant-HJ/whosthatpokemon/main/images/hidden/{poke_id:>03}.png'
        rev_img = f'https://raw.githubusercontent.com/Hemant-HJ/whosthatpokemon/main/images/revealed/{poke_id:>03}.png'
        species_data = await self.get_data(poke_id)
        names_data = species_data.get("names", [{}])
        eligible_names = [x["name"].lower() for x in names_data]
        english_name = [x["name"] for x in names_data if x["language"]["name"] == "en"][0]
        
        e = discord.Embed(
            title = 'Whos that Pokemon!',
            description = 'Guess the pokemon Below within 30 seconds.',
            color = discord.Color.blue(),
            timestamp = discord.utils.utcnow()
        )
        e.set_image(url = h_img)
        msg = await ctx.send(embed = e)

        def check(msg: discord.Message) -> bool:
            return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

        try:
            guess = await ctx.bot.wait_for('message', check = check, timeout = 30)
        except asyncio.TimeoutError:
            e = discord.Embed()
            e.description = f"The Right answer was {english_name}."
            e.set_image(url = rev_img)
            await msg.edit(embed = e)

        if guess.content.lower() in eligible_names:
            e.description = f'The Answer was right. It is {english_name}.'
            e.set_image(url = rev_img)
            await msg.edit(embed = e)
    
async def setup(bot):
    await bot.add_cog(WTP(bot))