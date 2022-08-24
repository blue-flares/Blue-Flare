import discord

from cogs.mongo import MongoClient
from . import embed

import os
import asyncio

mogno = MongoClient()

class UsernameButton(discord.ui.View):
    def __init__(self, ctx, user, username, mode, embed):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.user = user
        self.username = username
        self.mode = mode
        self.embed = embed

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm_button_callback(self, button, interaction):
        if self.mode == 'set':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = self.username
            else:
                data = self.ctx.bot.mongo.mongo.datastructure
                data['username'] = username
            await self.ctx.bot.mongo.update(self.user.id, data)
            self.embed.title = 'Successful Data Update'
            self.embed.description = 'The following data has been updated.'
            self.embed.color = discord.Color.green()

            await interaction.response.edit_message(embed = self.embed, view = None)
        
        elif self.mode == 'reset':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = 'Not Set'
            else:
                data = self.ctx.bot.mongo.mongo.datastructure
            await self.ctx.bot.mongo.update(self.user.id, data)
            self.embed.title = 'Successful Data Update'
            self.embed.description = 'Following user\'s data have been reseted.'
            
            await interaction.response.edit_message(embed = self.embed, view = None)

    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel_button_callback(self, button, interaction):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True

class DonationButton(discord.ui.View):
    def __init__(self, ctx, users, data, mode, embed):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.users = users
        self.data = data
        self.mode = mode
        self.embed = embed
        
    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.success)
    async def confirm_button_callback(self, button, interaction):
        if self.mode == 'add':
            for user in self.users:
                data = await self.ctx.bot.mongo.fetch(user)
                if data:
                    data['donation'] += self.data
                    await self.ctx.bot.mongo.update(a, data)
                else:
                    data = self.ctx.bot.mongo.mongo.datastructure
                    data['donation'] = self.data
                    await self.ctx.bot.mongo.update(a, data)
        
        elif self.mode == 'remove':
            for user in self.users:
                data = await self.ctx.bot.mongo.fetch(user)
                if data:
                    data['donation'] -= self.data
                    await self.ctx.bot.mongo.update(a, data)
                else:
                    await self.ctx.send(f'<@{user}> have no data entry in the database.')
        
        elif self.mode == 'set':
            for user in self.users:
                data = await self.ctx.bot.mongo.fetch(user)
                if data:
                    data['donation'] = self.data
                    await self.ctx.bot.mongo.update(a, data)
                else:
                    data = self.ctx.mongo.mongo.datastructure
                    data['donation'] = self.data
                    await self.ctx.bot.mongo.update(a, data)

        elif self.mode == 'reset':
            for user in self.users:
                data = await self.ctx.bot.mongo.fetch(user)
                if data:
                    data['donation'] = 0
                    await self.ctx.bot.mongo.update(a, data)
                else:
                    await self.ctx.send(f'<@{user}> have no entry in the database.')
        
        else:
            return
        
        self.embed.title = 'Successful Data Update'
        self.embed.description = 'The following things have been updated.'

        await interaction.response.edit_message(embed = self.embed, view = None)
    
    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel_button_callback(self, button, interaction):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.'. ephemeral = True)
        return True