import discord
from discord.ext import commands
from structures import TreeNode

class Discussion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_discussions = {}
        self.init_tree()

    def init_tree(self):
        root = TreeNode("Aimes-tu le développement Web ?", True, "web")
        
        left_web = TreeNode("Préfères-tu le visuel et l'interface ?", True, "frontend")
        right_no_web = TreeNode("Aimes-tu l'analyse de données ?", True, "data")
        
        res_html = TreeNode("Tu devrais apprendre HTML, CSS et JavaScript !", False, "javascript")
        res_backend = TreeNode("Tu devrais apprendre PHP ou Node.js !", False, "backend")
        
        res_python = TreeNode("Tu devrais apprendre Python !", False, "python")
        res_cpp = TreeNode("Tu devrais apprendre C++ ou Java !", False, "logiciel")

        root.left = left_web
        root.right = right_no_web
        
        left_web.left = res_html
        left_web.right = res_backend
        
        right_no_web.left = res_python
        right_no_web.right = res_cpp
        
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

