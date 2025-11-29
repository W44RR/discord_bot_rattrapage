import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from structures import LinkedList

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

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='last')
async def last(ctx):
    last_command = command_history.get_last()
    if last_command:
        await ctx.send(f"Dernière commande: {last_command}")
    else:
        await ctx.send("Rien dans l'historique.")
