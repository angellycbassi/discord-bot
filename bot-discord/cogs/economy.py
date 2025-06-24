"""
Cog: Economia e Loja In-Game
Moedas, lojas, leilões, badges, conquistas, transferências e taxas.
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, Any
from bot import economia_group

class Economy(commands.Cog):
    """
    Economia e Loja In-Game (slash commands).
    """
    def __init__(self, bot):
        self.bot = bot
        self.economy: Dict[int, Any] = {}

    @economia_group.command(name="transferir", description="Transfere moedas para outro jogador.")
    async def transferir(self, interaction: discord.Interaction, usuario: discord.Member, quantidade: int):
        await interaction.response.send_message(f"(Exemplo) Transferido {quantidade} moedas para {usuario.mention}.", ephemeral=True)

    @economia_group.command(name="loja", description="Exibe a loja in-game.")
    async def loja(self, interaction: discord.Interaction):
        await interaction.response.send_message("(Exemplo) Loja aberta!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Economy(bot))
