"""
Cog: Núcleo de Personagem Avançado
Permite múltiplas fichas por usuário, campos customizáveis, templates de sistemas e integração com campanhas.
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict, Any
from bot import personagem_group, CriarFichaModal
from database import listar_personagens

class EditarFichaModal(discord.ui.Modal, title="Editar Lenda"):
    def __init__(self, ficha_id: int, campo: str):
        super().__init__()
        self.ficha_id = ficha_id
        self.campo = campo
        self.valor = discord.ui.TextInput(
            label=f"Novo valor para {campo}",
            placeholder=f"Digite o novo valor para {campo}...",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.valor)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Aqui você implementaria a lógica de edição no banco
            embed = discord.Embed(
                title="✨ Lenda Modificada!",
                description=f"O campo **{self.campo}** da ficha **{self.ficha_id}** foi atualizado para: {self.valor.value}",
                color=discord.Color.green()
            )
            embed.set_footer(text="As histórias mudam, as lendas evoluem...")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao editar ficha: {str(e)}", ephemeral=True)

class GerenciarTemplateModal(discord.ui.Modal, title="Gerenciar Template de RPG"):
    nome = discord.ui.TextInput(label="Nome do Template", placeholder="Ex: D&D 5e, Tormenta20...", max_length=32)
    campos = discord.ui.TextInput(
        label="Campos do Template",
        placeholder="Ex: Força, Destreza, HP...\nUm campo por linha",
        style=discord.TextStyle.paragraph,
        max_length=300
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 Template Criado!",
            description=f"Template **{self.nome.value}** registrado com sucesso!",
            color=discord.Color.gold()
        )
        campos_lista = self.campos.value.split('\n')
        embed.add_field(name="Campos", value="\n".join(f"• {campo}" for campo in campos_lista))
        embed.set_footer(text="Use este template ao criar novas fichas!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VerFichaView(discord.ui.View):
    def __init__(self, ficha_id: int):
        super().__init__(timeout=None)
        self.ficha_id = ficha_id

    @discord.ui.button(label="Editar", style=discord.ButtonStyle.primary, emoji="✏️")
    async def editar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditarFichaModal(self.ficha_id, "Campo"))

    @discord.ui.button(label="Remover", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Aqui você implementaria a remoção no banco
        embed = discord.Embed(
            title="💫 Lenda Encerrada",
            description=f"A história da ficha **{self.ficha_id}** chegou ao fim...",
            color=discord.Color.red()
        )
        embed.set_footer(text="Mas outras lendas aguardam para serem contadas!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class CharacterAdvanced(commands.Cog):
    """
    Núcleo de Personagem Avançado (slash commands).
    """
    def __init__(self, bot):
        self.bot = bot
        self.characters: Dict[int, List[Dict[str, Any]]] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}

    @personagem_group.command(name="criar", description="Cria uma nova ficha de personagem.")
    async def criar(self, interaction: discord.Interaction):
        # Reutiliza o modal já existente
        await interaction.response.send_modal(CriarFichaModal())

    @personagem_group.command(name="listar", description="Lista todas as fichas do usuário.")
    async def listar(self, interaction: discord.Interaction):
        try:
            fichas = listar_personagens(str(interaction.user.id))
            if not fichas:
                embed = discord.Embed(
                    title="📜 Nenhuma Lenda Encontrada!",
                    description="Você ainda não forjou nenhum herói para o seu grupo.",
                    color=discord.Color.red()
                )
            else:
                embed = discord.Embed(
                    title="🏰 Heróis do Seu Grimório",
                    color=discord.Color.purple(),
                    description="Estes são os aventureiros que já trilharam caminhos mágicos ao seu lado:"
                )
                for idx, (nome, raca, classe) in enumerate(fichas, 1):
                    embed.add_field(
                        name=f"{idx}. {nome}",
                        value=f"Raça: {raca}\nClasse: {classe}",
                        inline=False
                    )
                embed.set_footer(text="Que novas histórias você irá escrever?")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao listar fichas: {str(e)}", ephemeral=True)

    @personagem_group.command(name="editar", description="Edita uma ficha existente.")
    async def editar(self, interaction: discord.Interaction, ficha_id: int, campo: str):
        await interaction.response.send_modal(EditarFichaModal(ficha_id, campo))

    @personagem_group.command(name="remover", description="Remove uma ficha existente.")
    async def remover(self, interaction: discord.Interaction, ficha_id: int):
        view = VerFichaView(ficha_id)
        embed = discord.Embed(
            title="⚠️ Confirmar Remoção",
            description=f"Tem certeza que deseja remover a ficha **{ficha_id}**?\nEsta ação não pode ser desfeita!",
            color=discord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @personagem_group.command(name="template", description="Gerencia templates de sistemas de RPG.")
    async def template(self, interaction: discord.Interaction):
        await interaction.response.send_modal(GerenciarTemplateModal())

async def setup(bot):
    await bot.add_cog(CharacterAdvanced(bot))
