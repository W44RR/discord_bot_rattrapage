import discord
from discord.ext import commands
from structures import TreeNode

class Discussion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_discussions = {}
        self.init_tree()

    def init_tree(self):
        # Racine : Action ou pas ?
        root = TreeNode("Aimes-tu les animés de combat et d'action ?", True, "action")
        
        # Branche Action (Gauche = Oui)
        q_long_classic = TreeNode("Aimes-tu les classiques avec beaucoup d'épisodes ?", True, "classique")
        
        # Branche Non-Action (Droite = Non) -> Romance/Drame
        q_romance = TreeNode("Cherches-tu une histoire de romance émouvante ?", True, "romance")
        
        # Sous-branche Action -> Classique (Gauche = Oui)
        q_ninja = TreeNode("Préfères-tu les ninjas aux guerriers de l'espace ?", True, "ninja")
        res_jjk = TreeNode("Tu devrais regarder Jujutsu Kaisen !", False, "jujutsu kaisen")
        
        # Résultats Action
        res_naruto = TreeNode("Tu devrais regarder Naruto !", False, "naruto")
        res_dbz = TreeNode("Tu devrais regarder Dragon Ball Z !", False, "dbz")
        
        # Sous-branche Romance (Gauche = Oui)
        q_music = TreeNode("La musique est-elle importante pour toi ?", True, "musique")
        res_death_note = TreeNode("Alors essaie Death Note pour le suspense !", False, "death note")
        
        # Résultats Romance
        res_ylia = TreeNode("Tu devrais regarder Your Lie in April !", False, "your lie in april")
        res_golden_time = TreeNode("Tu devrais regarder Golden Time !", False, "golden time")

        # Construction de l'arbre
        root.left = q_long_classic
        root.right = q_romance
        
        # Action
        q_long_classic.left = q_ninja      # Oui classiques
        q_long_classic.right = res_jjk     # Non classiques (moderne)
        
        q_ninja.left = res_naruto          # Oui ninjas
        q_ninja.right = res_dbz            # Non (donc DBZ)
        
        # Romance / Autre
        q_romance.left = q_music           # Oui romance
        q_romance.right = res_death_note   # Non romance (donc thriller)
        
        q_music.left = res_ylia            # Oui musique
        q_music.right = res_golden_time    # Non musique

        self.bot.discussion_tree.set_root(root)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.id in self.user_discussions:
            current_node = self.user_discussions[message.author.id]
            content = message.content.lower()
            
            if content in ["oui", "non"]:
                next_node = None
                if content == "oui":
                    next_node = current_node.left
                else:
                    next_node = current_node.right
                
                if next_node:
                    if next_node.is_question:
                        self.user_discussions[message.author.id] = next_node
                        await message.channel.send(next_node.text)
                    else:
                        await message.channel.send(f"Résultat : {next_node.text}")
                        del self.user_discussions[message.author.id]
                else:
                    await message.channel.send("Erreur dans l'arbre, fin de la discussion.")
                    del self.user_discussions[message.author.id]

    @commands.command(name='help')
    async def start_discussion(self, ctx):
        self.user_discussions[ctx.author.id] = self.bot.discussion_tree.root
        await ctx.send(f"Début du questionnaire : {self.bot.discussion_tree.root.text} (Répondez par 'oui' ou 'non')")

    @commands.command(name='reset')
    async def reset_discussion(self, ctx):
        self.user_discussions[ctx.author.id] = self.bot.discussion_tree.root
        await ctx.send(f"Discussion réinitialisée : {self.bot.discussion_tree.root.text}")

    @commands.command(name='speak')
    async def speak_about(self, ctx, *args):
        if len(args) >= 2 and args[0] == "about":
            topic = " ".join(args[1:])
            found = self.bot.discussion_tree.search_topic(self.bot.discussion_tree.root, topic)
            if found:
                await ctx.send("Oui")
            else:
                await ctx.send("Non")
        else:
            await ctx.send("Usage: speak about <sujet>")

async def setup(bot):
    await bot.add_cog(Discussion(bot))

