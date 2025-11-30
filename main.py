import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from structures import LinkedList, DiscussionTree

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

bot.command_history = LinkedList()
bot.discussion_tree = DiscussionTree()

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await bot.load_extension('commandes.general')
    await bot.load_extension('commandes.history')
    await bot.load_extension('commandes.discussion')
    await bot.load_extension('commandes.persistence')
    await bot.load_extension('commandes.extras')
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    bot.run(token)
else:
    print("Erreur : Le token Discord n'a pas été trouvé dans le fichier .env")
if token:
    bot.run(token)
else:
    print("Erreur : Le token Discord n'a pas été trouvé dans le fichier .env")
