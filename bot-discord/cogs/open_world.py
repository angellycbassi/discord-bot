"""
Cog: Aventura de Mundo Aberto
Exploração solo/grupo, convites, eventos randômicos, bosses, loot, mapas visuais.
"""
import discord
from discord import app_commands
from discord.ext import commands, tasks
from typing import Dict, Any
from bot import aventura_group
import random
import datetime

class OpenWorld(commands.Cog):
    """
    Aventura de Mundo Aberto (slash commands).
    """
    def __init__(self, bot):
        self.bot = bot
        self.adventures: Dict[int, Any] = {}
        self.bosses: Dict[int, Any] = {}
        self.maps: Dict[int, Any] = {}
        self.active_event: Dict[str, Any] = {}
        self.event_loop.start()

    @tasks.loop(minutes=30)
    async def event_loop(self):
        now = datetime.datetime.now()
        if random.random() < 0.5:
            event = random.choice([
                {"nome": "Boss Global: Dragão Ancião", "descricao": "Um dragão ameaça todos os jogadores!"},
                {"nome": "Invasão Goblin", "descricao": "Goblins invadiram o reino!"},
                {"nome": "Festival Sazonal", "descricao": "Celebre e ganhe recompensas!"}
            ])
            self.active_event = event
            for guild in self.bot.guilds:
                channel = discord.utils.get(guild.text_channels, name="geral")
                if channel:
                    await channel.send(f"⚔️ **Evento Mundial Ativo:** {event['nome']}\n{event['descricao']}")

    @aventura_group.command(name="iniciar", description="Inicia uma aventura solo ou em grupo.")
    async def iniciar(self, interaction: discord.Interaction, solo: bool = True):
        await interaction.response.send_message(f"(Exemplo) Aventura iniciada. Solo: {solo}", ephemeral=True)

    @aventura_group.command(name="convidar", description="Convida outro jogador para a aventura.")
    async def convidar(self, interaction: discord.Interaction, usuario: discord.Member):
        await interaction.response.send_message(f"(Exemplo) Convite enviado para {usuario.mention}.", ephemeral=True)

    @aventura_group.command(name="mapa", description="Exibe o mapa visual do mundo.")
    async def mapa(self, interaction: discord.Interaction):
        await interaction.response.send_message("(Exemplo) Exibindo mapa do mundo...", ephemeral=True)

    @aventura_group.command(name="boss", description="Enfrenta um boss durante a aventura.")
    async def boss(self, interaction: discord.Interaction):
        await interaction.response.send_message("(Exemplo) Boss encontrado!", ephemeral=True)

    @aventura_group.command(name="evento", description="Mostra o evento mundial ativo.")
    async def evento(self, interaction: discord.Interaction):
        if self.active_event:
            embed = discord.Embed(title=f"🌍 Evento Ativo: {self.active_event['nome']}", description=self.active_event['descricao'], color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            await interaction.response.send_message("Nenhum evento mundial ativo no momento.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(OpenWorld(bot))
