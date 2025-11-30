import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from structures import LinkedList, DiscussionTree

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

bot.command_history = LinkedList()
bot.discussion_tree = DiscussionTree()

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await bot.load_extension('cogs.general')
    await bot.load_extension('cogs.history')
    await bot.load_extension('cogs.discussion')
    await bot.load_extension('cogs.persistence')
    await bot.load_extension('cogs.extras')

token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("Erreur : Le token Discord n'a pas été trouvé dans le fichier .env")
if token:
    bot.run(token)
else:
    print("Erreur : Le token Discord n'a pas été trouvé dans le fichier .env")
