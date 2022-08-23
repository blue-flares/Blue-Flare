import discord

from cogs.mongo import MongoClient
from . import embed

import os
import asyncio

mogno = MongoClient()

class UsernameButton(discord.ui.View):
    def __init__(self, ctx, user, username, mode):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.user = user
        self.username = username
        self.mode = mode

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm_button_callback(self, button, interaction):
        if self.mode == 'set':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = self.username
            else:
                data = self.ctx.bot.mongo.mongo.datastructure
                data['username'] = self.username
            await self.ctx.bot.mongo.update(self.user.id, data)
            e = embed.data_update(self.ctx, 'Successful Update', discord.Color.green())
            e.description = 'The following data has been updated.'
            e.add_field(name = 'User', value = f'<@{self.user.id}>', inline = False)
            e.add_field(name = 'Value', value = self.username.title(), inline = False)
            e.add_field(name = 'Responsible Editor', value = f'<@{self.ctx.author.id}>', inline = False)

            await interaction.response.edit_message(embed = e, view = None)
        
        elif self.mode == 'reset':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = 'Not Set'
            else:
                data = self.ctx.bot.mongo.mongo.datastructure
            await self.ctx.bot.mongo.update(self.user.id, data)
            e = embed.data_update(self.ctx, 'Successful Update', discord.Color.green())
            e.description = 'Following user\'s data have been reseted.'
            e.add_field(name = 'User', value = f'<@{self.user.id}>', inline = False)
            e.add_field(name = 'Responsible Editor', value = f'<@{self.ctx.author.id}>', inline = False)

            await interaction.response.edit_message(embed = e, view = None)

    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel_button_callback(self, button, interaction):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True

class DonationButton(discord.ui.View):
    def __init__(self, ctx, users, data, mode):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.users = users
        self.data = data
        self.mode = mode
        
    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.success)
    async def confirm_button_callback(self, button, interaction):
        pass