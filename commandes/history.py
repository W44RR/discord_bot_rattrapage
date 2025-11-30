import discord
from discord.ext import commands

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
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

    @commands.command(name='history')
    async def command_history(self, ctx):
        all_cmds = self.bot.command_history.get_all()
        if all_cmds:
            history = "\n".join(all_cmds)
            await ctx.send(f"Historique des commandes:\n{history}")
        else:
            await ctx.send("Rien dans l'historique.")

    @commands.command(name='clear_history')
    async def clear_history(self, ctx):

        self.bot.command_history.clear()
        await ctx.send("Historique des commandes effacé.")

async def setup(bot):
    await bot.add_cog(History(bot))