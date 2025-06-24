"""
Cog: Integração com Inteligência Artificial
NPCs controlados por IA, diálogos dinâmicos, sugestões automáticas de eventos.
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, Any
from bot import ia_group

class AIIntegration(commands.Cog):
    """
    Integração com IA (slash commands).
    """
    def __init__(self, bot):
        self.bot = bot
        self.npcs: Dict[int, Any] = {}

    @ia_group.command(name="npc", description="Envia uma mensagem de um NPC controlado por IA.")
    async def npc(self, interaction: discord.Interaction, nome: str, mensagem: str):
        class NPCView(discord.ui.View):
            @discord.ui.button(label="Responder", style=discord.ButtonStyle.primary, emoji="💬")
            async def responder(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                await interaction_button.response.send_modal(
                    discord.ui.Modal(
                        title=f"Responder ao NPC {nome}",
                        components=[
                            discord.ui.InputText(
                                label="Sua resposta",
                                placeholder="Digite sua resposta ao NPC...",
                                style=discord.InputTextStyle.long,
                                required=True
                            )
                        ]
                    )
                )

        embed = discord.Embed(
            title=f"🧙‍♂️ NPC: {nome}",
            description=f"{mensagem}\n\n*Clique em 💬 para responder ao NPC!*",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/616/616494.png")
        embed.set_footer(text="Mensagem enviada por um NPC controlado por IA • RPGium", icon_url="https://cdn-icons-png.flaticon.com/512/616/616494.png")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=NPCView())

    @ia_group.command(name="sugerir_evento", description="Sugere um evento/desafio baseado na campanha.")
    async def sugerir_evento(self, interaction: discord.Interaction, campanha_id: int):
        class EventoView(discord.ui.View):
            @discord.ui.button(label="Nova Sugestão", style=discord.ButtonStyle.success, emoji="🎲")
            async def nova_sugestao(self, interaction_button: discord.Interaction, button: discord.ui.Button):
                # Exemplo de sugestões dinâmicas
                import random
                sugestoes = [
                    "⚔️ Um bando de goblins saqueia uma vila próxima!",
                    "🐉 Um dragão desperta nas montanhas!",
                    "🧙‍♂️ Um mago misterioso oferece uma missão secreta.",
                    "🏰 Um castelo antigo revela passagens ocultas.",
                    "💎 Um artefato lendário foi avistado em ruínas esquecidas."
                ]
                sugestao = random.choice(sugestoes)
                embed = discord.Embed(
                    title="📜 Nova Sugestão de Evento!",
                    description=f"⚔️ **Campanha:** `{campanha_id}`\n\n{sugestao}\n\n*Clique novamente para mais ideias!*",
                    color=discord.Color.gold()
                )
                embed.set_footer(text="Sugestão gerada por IA • RPGium", icon_url="https://cdn-icons-png.flaticon.com/512/616/616494.png")
                await interaction_button.response.edit_message(embed=embed, view=self)

        embed = discord.Embed(
            title="📜 Sugestão de Evento Épico!",
            description=(
                f"⚔️ **Campanha:** `{campanha_id}`\n\n"
                "Um novo desafio surge no horizonte! Que tal enfrentar um dragão ancestral, proteger uma vila ameaçada ou buscar um artefato lendário?\n\n"
                "*Clique em 🎲 para gerar outra sugestão!*"
            ),
            color=discord.Color.gold()
        )
        embed.set_image(url="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80")
        embed.set_footer(text="Sugestão gerada por IA • RPGium", icon_url="https://cdn-icons-png.flaticon.com/512/616/616494.png")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=EventoView())

async def setup(bot):
    await bot.add_cog(AIIntegration(bot))
