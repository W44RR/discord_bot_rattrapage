import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from structures import LinkedList, DiscussionTree

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='+', intents=intents)
        self.command_history = LinkedList()
        self.discussion_tree = DiscussionTree()

    async def setup_hook(self):
        await self.load_extension('commandes.history')
        await self.load_extension('commandes.discussion')

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Connecté en tant que  {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    try:
        bot.run(token)
    except discord.errors.PrivilegedIntentsRequired:
        print("\n[ERREUR] Les 'Privileged Intents' sont requis mais non activés.")
        print("Veuillez activer 'Message Content Intent' sur le portail développeur Discord.")
        print("Allez sur: https://discord.com/developers/applications/ -> Votre App -> Bot -> Privileged Gateway Intents\n")
else:
    print("Le token du bot n'a pas été trouvé.")

