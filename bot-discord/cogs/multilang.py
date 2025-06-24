"""
Cog: Suporte Multilíngue
Tradução de comandos, painéis e mensagens, escolha de idioma por servidor.
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, Any
from bot import idioma_group

class MultiLang(commands.Cog):
    """
    Suporte Multilíngue (slash commands).
    """
    def __init__(self, bot):
        self.bot = bot
        self.languages: Dict[int, str] = {}

    @idioma_group.command(name="definir", description="Define o idioma do servidor.")
    async def definir(self, interaction: discord.Interaction, idioma: str):
        await interaction.response.send_message(f"(Exemplo) Idioma definido para {idioma}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MultiLang(bot))
