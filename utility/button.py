import discord

class UsernameButton(discord.ui.View):
    def __init__(self, ctx, user, username, mode, embed):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.user = user
        self.username = username
        self.mode = mode
        self.embed = embed

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.mode == 'set':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = self.username
            else:
                data = self.ctx.bot.mongo.mongo.datastructure
                data['username'] = self.username
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
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction: discord.Interaction):
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

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button ):
        for user in self.users:
            data = await self.ctx.bot.mongo.fetch(user)
            if data:
                if self.mode == 'add':
                    data['donation'] += self.data
                elif self.mode == 'remove':
                    data['donation'] -= self.data
                elif self.mode == 'set':
                    data['donation'] = self.data
                elif self.mode == 'reset':
                    data['donation'] = 0
                await self.ctx.bot.mongo.update(user, data)

            else:
                await self.ctx.send(f'<@{user}> has no data entry in database. \nPlease add username first.')

        self.embed.title = 'Successful Data Update'
        self.embed.description = 'Following things have been updated'
        self.embed.color = discord.Color.green()

        await interaction.response.edit_message(embed = self.embed, view = None)
    
    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True

class BattleButton(discord.ui.View):
    def __init__(self, ctx, users, data, mode, embed, result):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.users = users
        self.data = data
        self.embed = embed
        self.mode = mode
        self.result = result

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        for user in self.users:
            data = await self.ctx.bot.mongo.fetch(user)
            if data:
                if self.mode == 'add':
                    data[self.result] += self.data
                elif self.mode == 'remove':
                    data[self.result] -= self.data
                elif self.mode == 'set':
                    data[self.result] = self.data
                elif self.mode == 'reset':
                    data[self.result] = 0

                await self.ctx.bot.mongo.update(user, data)
            else:
                await self.ctx.send(f'<@{user}> have no entry in database.\nPlease add the username first.')

        self.embed.color = discord.Color.green()
        self.embed.title = 'Successful Data Update'
        self.embed.description = 'Following things will be updated.'

        await interaction.response.edit_message(embed = self.embed, view = None)

    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True

class ChatButton(discord.ui.View):
    def __init__(self, ctx, users, data, mode, embed):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.users = users
        self.data = data
        self.embed = embed
        self.mode = mode 

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        for user in self.users:
            data = await self.ctx.bot.mongo.fetch(user)
            if data:
                if self.mode == 'add':
                    data['chat'] += self.data
                elif self.mode == 'remove':
                    data['chat'] -= self.data
                elif self.mode == 'set':
                    data['chat'] = self.data
                elif self.mode == 'reset':
                    data['chat'] = 0

                await self.ctx.bot.mongo.update(user, data)
            else:
                await self.ctx.send(f'<@{user}> have no entry in database.\nPlease add the username first.')

        self.embed.color = discord.Color.green()
        self.embed.title = 'Successful Data Update'
        self.embed.description = 'Following things will be updated.'

        await interaction.response.edit_message(embed = self.embed, view = None)

    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True