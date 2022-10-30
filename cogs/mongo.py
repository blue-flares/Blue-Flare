import discord
from discord.ext import commands

import config 

import pymongo

class MongoClient:
    def __init__(self):
        self.client = pymongo.MongoClient(config.MAIN)
        self.db = self.client['BlueFlare']
        self.col = self.db['Main']
        self.settings = self.db['Setting']
        self.datastructure = {'username': 'Not Set', 'donation': 0, 'win': 0, 'lose': 0, 'draw': 0, 'chat': 0}

class Mongo(commands.Cog, MongoClient):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.mongo = MongoClient()

    async def insert(self, data: dict):
        data = self.mongo.col.insert_one(data)
        return data

    async def fetch(self, _id):
        data = self.mongo.col.find_one({'_id': _id})
        return data

    async def update(self, _id, data: dict):
        data = self.mongo.col.update_one({'_id': _id}, {'$set': data}, upsert = True)
        return data 

    async def delete(self, _id):
        data = self.mongo.col.delete_one({'_id': _id})
        return data

async def setup(bot):
    await bot.add_cog(Mongo(bot))