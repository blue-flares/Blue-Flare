import random
import asyncio
from contextlib import suppress

import aiohttp
import discord
from discord.ext import commands

class Wtp(commands.Cog):
    """ Who's That Pokemon! """
    def __init__(self, bot):
        self.bot = bot
        self.unanswered = 0

    async def cog_unload(self):
        await self.bot.session.close()
        
    async def get_img(self):
        poke_id = random.randint(1, 900)
        img_h = f'https://raw.githubusercontent.com/Hemant-HJ/whosthatpokemon/main/images/hidden/{poke_id:>03}.png'
        img_r = f'https://raw.githubusercontent.com/Hemant-HJ/whosthatpokemon/main/images/revealed/{poke_id:>03}.png'
        
        return img_h, img_r, poke_id

    async def get_name(self, url):
        async with self.bot.session.get(url) as response:
            return await response.json(content_type=None)

    @commands.command()
    async def wtp(self, ctx, number:int = 1):
        for time in range(number):
            imgs = await self.get_img()

            e = discord.Embed(
                title = "Who's That Pokemon.",
                description = "Guess the pokemon within 30secs. You get 3 chances to guess.",
                color = discord.Color.red(),
                timestamp = discord.utils.utcnow()
            )
            e.set_image(url = imgs[0])

            msg = await ctx.send(embed = e)

            species_data = await self.get_name(f'https://pokeapi.co/api/v2/pokemon-species/{imgs[2]}')
            names = species_data.get('names', [{}])
            eligible_names = [x["name"].lower() for x in names]
            english_name = [x["name"] for x in names if x["language"]["name"] == "en"][0]

            def check(msg):
                return msg.channel.id == ctx.channel.id

            attempt = 0
            while attempt != 3:
                try:
                    guess = await ctx.bot.wait_for('message', timeout = 10, check = check)
                except asyncio.TimeoutError:
                    attempt = 3
                    e = discord.Embed(
                        title = 'You were not able to guess the right answer.',
                        description = f"It was **{english_name}**",
                        color = discord.Color.red(),
                        timestamp = discord.utils.utcnow()
                    )
                    e.set_image(url = imgs[1])
                    self.unanswered += 1
                    await ctx.send(embed = e)
                    if self.unanswered == 3:
                        e = discord.Embed(
                            title = 'Game Stopped',
                            description = "Who's that Pokemon game has been stopped because of 3 unanswered question you can restart it using the command.\n\n`bf wtp <count = 1>`",
                            timestamp = discord.utils.utcnow(),
                            color = discord.Color.red()
                        )
                        return await ctx.send(embed = e)
                    elif time + 1 == number:
                        return
                    else:
                        continue
                
                if guess.content.lower() in eligible_names:
                    attempt = 3
                    right_ans = True
                else:
                    attempt += 1
                    right_ans = False
                
                if attempt == 3:
                    e = discord.Embed(
                        title = 'You got it right!!' if right_ans else 'You were not able to guess the right answer.',
                        description = f"It was **{english_name}**",
                        color = discord.Color.green() if right_ans else discord.Color.red(),
                        timestamp = discord.utils.utcnow()
                        )
                    e.set_image(url = imgs[1])
                    await ctx.send(embed = e)

            await asyncio.sleep(2)

async def setup(bot):
    await bot.add_cog(Wtp(bot))