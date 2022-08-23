import discord
from discord.ext import commands

import config

import asyncio 
import pymongo

class MongoClient:
    def __init__(self):
        self.client = pymongo.MongoClient(config.MAIN)
        self.db = self.client['BlueFlare']
        self.col = self.db['Main']
        self.settings = self.db['Setting']
        self.datastructure = {'username': 'Not Set', 'win': 0, 'lose': 0, 'draw': 0}

class Mongo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo = MongoClient()


    async def fetch(self, _id):
        data = self.mongo.col.find_one({'_id': _id})
        return data

    async def update(self, _id, data:dict):
        data = self.mongo.col.update_one({'_id': _id}, {'$set': data}, upsert = True)
        return data 

    async def delete(self, _id):
        data = self.mongo.col.delete_one({'_id': _id})
        return data

def setup(bot):
    bot.add_cog(Mongo(bot))