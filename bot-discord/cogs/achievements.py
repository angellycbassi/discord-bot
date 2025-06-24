import discord
from discord.ext import commands
from typing import Dict, Any, List

class Achievements(commands.Cog):
    """
    Cog: Conquistas, Badges, Títulos e Medalhas
    Permite visualizar, desbloquear e notificar conquistas no Discord.
    """
    def __init__(self, bot):
        self.bot = bot
        self.achievements: Dict[int, List[Dict[str, Any]]] = {}

    @commands.group(name="conquistas", invoke_without_command=True)
    async def conquistas(self, ctx):
        """Mostra as conquistas do usuário."""
        user_id = ctx.author.id
        conquistas = self.achievements.get(user_id, [])
        embed = discord.Embed(title="🏆 Suas Conquistas", color=discord.Color.gold())
        if not conquistas:
            embed.description = "Nenhuma conquista desbloqueada ainda."
        else:
            for c in conquistas:
                embed.add_field(name=f"{c['icon']} {c['nome']}", value=c['descricao'], inline=False)
        await ctx.send(embed=embed)

    @conquistas.command(name="desbloquear")
    async def desbloquear(self, ctx, nome: str):
        """Desbloqueia uma conquista pelo nome (exemplo para testes)."""
        user_id = ctx.author.id
        conquistas = self.achievements.setdefault(user_id, [])
        nova = {"nome": nome, "descricao": f"Conquista especial: {nome}", "icon": "🎖️"}
        conquistas.append(nova)
        embed = discord.Embed(
            title="🏅 Nova Conquista!",
            description=f"Você desbloqueou: **{nome}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Descrição", value=nova["descricao"])
        await ctx.send(embed=embed)
        try:
            await ctx.author.send(f"Parabéns! Você desbloqueou a conquista: {nome} 🎉")
        except Exception:
            pass

async def setup(bot):
    await bot.add_cog(Achievements(bot))
