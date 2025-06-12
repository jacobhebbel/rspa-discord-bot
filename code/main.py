import os
import discord
from dotenv import load_dotenv

load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()