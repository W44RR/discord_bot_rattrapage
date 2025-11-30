import discord
from discord.ext import commands, tasks
import json
import os

class Persistence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = 'data/history.json'
        self.auto_save.start()

    def cog_unload(self):
        self.auto_save.cancel()

    def save_to_json(self):
        history_list = self.bot.command_history.get_all()
        
        data = {
            "history": history_list
        }

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print("Données sauvegardées.")

    def load_from_json(self):
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if "history" in data:
                    self.bot.command_history.clear() # On vide d'abord
                    for item in data["history"]:
                        self.bot.command_history.add(item)
            print("Données chargées.")
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")

    @tasks.loop(minutes=1.0)
    async def auto_save(self):
        self.save_to_json()

    @commands.Cog.listener()
    async def on_ready(self):
        self.load_from_json()

    @commands.command(name='save')
    async def manual_save(self, ctx):
        """Sauvegarde manuellement les données"""
        self.save_to_json()
        await ctx.send("Données sauvegardées avec succès !")

async def setup(bot):
    await bot.add_cog(Persistence(bot))
