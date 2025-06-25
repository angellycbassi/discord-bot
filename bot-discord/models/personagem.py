from discord import app_commands, Interaction
import discord
from database import listar_personagens, criar_personagem, set_avatar_personagem, get_avatar_personagem

personagem_group = app_commands.Group(name="personagem", description="Gerencie fichas de personagem")

# Painel interativo de personagem
@personagem_group.command(name="painel", description="Abre o painel interativo de personagem.")
async def personagem_painel(interaction: Interaction):
    await interaction.response.send_message(
        "[Acessível] Painel de personagem:",
        view=PersonagemPainelView(interaction.user.id),
        ephemeral=True
    )

class PersonagemPainelView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.add_item(CriarFichaButton(user_id))
        fichas = listar_personagens(str(user_id))
        if fichas:
            for idx, (nome, *_rest) in enumerate(fichas, 1):
                self.add_item(VerFichaButton(idx, nome, user_id))
                self.add_item(RemoverFichaButton(idx, nome, user_id))

class CriarFichaButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Criar Ficha", style=discord.ButtonStyle.success)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(CriarFichaModal(self.user_id))

class CriarFichaModal(discord.ui.Modal, title="Criar Nova Ficha"):
    nome = discord.ui.TextInput(label="Nome do personagem", max_length=30)
    async def on_submit(self, interaction: Interaction):
        criar_personagem(str(interaction.user.id), self.nome.value)
        await interaction.response.send_message(f"[Acessível] Ficha '{self.nome.value}' criada com sucesso!", ephemeral=True)

class VerFichaButton(discord.ui.Button):
    def __init__(self, idx, nome, user_id):
        super().__init__(label=f"Ver: {nome}", style=discord.ButtonStyle.primary)
        self.idx = idx
        self.nome = nome
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        fichas = listar_personagens(str(self.user_id))
        personagem = fichas[self.idx - 1]
        nome, raca, classe, xp, nivel, status = personagem
        embed = discord.Embed(title=f"Ficha de {nome}", description=f"Raça: {raca}\nClasse: {classe}\nXP: {xp}\nNível: {nivel}\nStatus: {status}")
        avatar_url = get_avatar_personagem(self.idx)
        if avatar_url:
            embed.set_thumbnail(url=avatar_url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class RemoverFichaButton(discord.ui.Button):
    def __init__(self, idx, nome, user_id):
        super().__init__(label=f"Remover: {nome}", style=discord.ButtonStyle.danger)
        self.idx = idx
        self.nome = nome
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(RemoverFichaModal(self.user_id, self.idx, self.nome))

class RemoverFichaModal(discord.ui.Modal, title="Remover Ficha"):
    def __init__(self, user_id, idx, nome):
        super().__init__()
        self.user_id = user_id
        self.idx = idx
        self.nome = nome
        self.confirm = discord.ui.TextInput(label=f"Digite o nome '{self.nome}' para confirmar", max_length=30)
        self.add_item(self.confirm)
    async def on_submit(self, interaction: Interaction):
        if self.confirm.value == self.nome:
            # Aqui você pode implementar a função de remoção real
            await interaction.response.send_message(f"[Acessível] Ficha '{self.nome}' removida (simulação).", ephemeral=True)
        else:
            await interaction.response.send_message("[Acessível] Nome não confere. Operação cancelada.", ephemeral=True)

# Comando avatar já existente
@personagem_group.command(name="avatar", description="Defina o avatar de uma ficha de personagem.")
@app_commands.describe(ficha_id="ID da ficha para definir o avatar")
async def personagem_avatar(interaction: Interaction, ficha_id: int):
    fichas = listar_personagens(str(interaction.user.id))
    if not fichas or ficha_id < 1 or ficha_id > len(fichas):
        await interaction.response.send_message("Ficha não encontrada.", ephemeral=True)
        return
    await interaction.response.send_modal(AvatarPersonagemModal(ficha_id))

class AvatarPersonagemModal(discord.ui.Modal, title="Avatar do Personagem"):
    def __init__(self, ficha_id):
        super().__init__()
        self.ficha_id = ficha_id
        self.url = discord.ui.TextInput(label="URL da Imagem do Avatar", placeholder="Cole o link da imagem (jpg/png)", max_length=200)
        self.add_item(self.url)
    async def on_submit(self, interaction: discord.Interaction):
        set_avatar_personagem(self.ficha_id, self.url.value)
        embed = discord.Embed(
            title="Avatar Atualizado",
            description="O avatar da ficha foi salvo! Ele aparecerá nos detalhes da ficha.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=self.url.value)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Adicione aqui outros comandos do grupo personagem conforme necessário.
