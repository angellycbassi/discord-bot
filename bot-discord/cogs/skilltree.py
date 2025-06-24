import discord
from discord.ext import commands
from typing import List, Dict, Any

class SkillTree(commands.Cog):
    """
    Cog: Árvore de Habilidades
    Permite visualizar, desbloquear e evoluir habilidades via comandos e botões no Discord.
    """
    def __init__(self, bot):
        self.bot = bot
        # Exemplo de estrutura de árvore (pode ser carregada do banco)
        self.skill_trees: Dict[int, List[Dict[str, Any]]] = {}

    @commands.group(name="skills", invoke_without_command=True)
    async def skills(self, ctx):
        """Mostra a árvore de habilidades do personagem."""
        user_id = ctx.author.id
        tree = self.skill_trees.get(user_id, [
            {"id": "root", "name": "Aptidão Básica", "unlocked": True, "children": [
                {"id": "atk1", "name": "Ataque Rápido", "unlocked": False},
                {"id": "def1", "name": "Defesa Básica", "unlocked": False}
            ]}
        ])
        embed = discord.Embed(title="🌳 Árvore de Habilidades", color=discord.Color.blurple())
        def render(nodes, depth=0):
            for n in nodes:
                prefix = "  " * depth + ("✔️ " if n.get("unlocked") else "❌ ")
                embed.add_field(name=prefix + n["name"], value=f"ID: {n['id']}", inline=False)
                if n.get("children"):
                    render(n["children"], depth+1)
        render(tree)
        await ctx.send(embed=embed)

    @skills.command(name="unlock")
    async def unlock(self, ctx, skill_id: str):
        """Desbloqueia uma habilidade pelo ID."""
        user_id = ctx.author.id
        tree = self.skill_trees.setdefault(user_id, [
            {"id": "root", "name": "Aptidão Básica", "unlocked": True, "children": [
                {"id": "atk1", "name": "Ataque Rápido", "unlocked": False},
                {"id": "def1", "name": "Defesa Básica", "unlocked": False}
            ]}
        ])
        def unlock_skill(nodes):
            for n in nodes:
                if n["id"] == skill_id:
                    n["unlocked"] = True
                    return True
                if n.get("children") and unlock_skill(n["children"]):
                    return True
            return False
        if unlock_skill(tree):
            await ctx.send(f"🔓 Habilidade `{skill_id}` desbloqueada!")
        else:
            await ctx.send(f"❌ Habilidade `{skill_id}` não encontrada.")

async def setup(bot):
    await bot.add_cog(SkillTree(bot))
