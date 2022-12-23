import os
from dotenv import load_dotenv

load_dotenv()

MAIN = os.getenv('MONGO_URI')
TOKEN = os.getenv('TOKEN')
