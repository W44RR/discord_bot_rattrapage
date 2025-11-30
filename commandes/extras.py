import discord
from discord.ext import commands
import random

class Extras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Fonctionnalité Bonus 1 : Jeu de dés
    @commands.command(name='roll')
    async def roll_dice(self, ctx, sides: int = 6):
        """Lance un dé à N faces (par défaut 6)"""
        if sides < 2:
            await ctx.send("Le dé doit avoir au moins 2 faces !")
            return
        result = random.randint(1, sides)
        await ctx.send(f"🎲 Vous avez lancé un dé à {sides} faces et obtenu : **{result}**")

    # Fonctionnalité Bonus 2 : Inversion de texte
    @commands.command(name='reverse')
    async def reverse_text(self, ctx, *, text: str):
        """Renvoie le texte inversé"""
        reversed_text = text[::-1]
        await ctx.send(f"🔄 : {reversed_text}")

    # Fonctionnalité Bonus 3 : Infos du serveur
    @commands.command(name='serverinfo')
    async def server_info(self, ctx):
        """Affiche les informations du serveur"""
        guild = ctx.guild
        embed = discord.Embed(title=f"Infos du serveur {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Membres", value=guild.member_count, inline=True)
        embed.add_field(name="Salons", value=len(guild.channels), inline=True)
        
        # Gestion sécurisée du propriétaire (peut être None sans les intents)
        if guild.owner:
            embed.add_field(name="Propriétaire", value=guild.owner.name, inline=True)
        else:
            embed.add_field(name="Propriétaire", value=f"ID: {guild.owner_id}", inline=True)
            
        embed.set_footer(text=f"ID: {guild.id}")
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Extras(bot))
