import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from structures import linkedList

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)

command_history = LinkedList()

@bot.event
async def on_ready():
    print(f'Connecté en tant que  {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('+'):
        command_history.add(f"{message.author.name}: {message.content}")
    
    await bot.process_commands(message)