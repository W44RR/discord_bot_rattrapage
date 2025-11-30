import discord
from discord.ext import commands

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.commandes.listener()
    async def on_message(self, message):
        if message.autho == self.bot.user:
            return
        if message.content.startswith('+'):
            self.bot.command_history.add(f"{message.author.name}: {message.content}")
        
    @commands.command(name='last')
    async def last_command  (self, ctx):
        last_cmd = self.bot.command_history.get_last()
        if last_cmd:
            await ctx.send(f"Dernière commande: {last_cmd}")
        else:
            await ctx.send("Rien dans l'historique.")
            