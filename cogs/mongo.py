import pymongo
import discord
from discord.ext import commands

import config

class MongoClient:
    """ Defines all the collections """
    def __init__(self):
        self.client = pymongo.MongoClient(config.MAIN)
        self.database = self.client['Blue-Flare']
        self.col = self.database['UserData']
        self.settings = self.database['Setting']
        