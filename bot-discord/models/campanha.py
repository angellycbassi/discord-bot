from discord import app_commands, Interaction
import discord
from database import listar_campanhas

campanha_group = app_commands.Group(name="campanha", description="Gerencie campanhas de RPG")

@campanha_group.command(name="painel", description="Abre o painel interativo de campanhas.")
async def campanha_painel(interaction: Interaction):
    await interaction.response.send_message(
        "[Acessível] Painel de campanhas:",
        view=CampanhaPainelView(interaction.user.id),
        ephemeral=True
    )

class CampanhaPainelView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.add_item(ListarCampanhasButton(user_id))
        self.add_item(CriarCampanhaButton(user_id))
        self.add_item(EntrarCampanhaButton(user_id))

class ListarCampanhasButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Listar Campanhas", style=discord.ButtonStyle.primary)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        campanhas = listar_campanhas(str(self.user_id))
        if not campanhas:
            await interaction.response.send_message("[Acessível] Você não participa de nenhuma campanha.", ephemeral=True)
            return
        msg = "\n".join([f"{nome}: {descricao or '(Sem descrição)'}" for camp_id, nome, descricao in campanhas])
        await interaction.response.send_message(f"Campanhas:\n{msg}", ephemeral=True)

class CriarCampanhaButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Criar Campanha", style=discord.ButtonStyle.success)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message("[Acessível] Em breve: painel de criação de campanha.", ephemeral=True)

class EntrarCampanhaButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Entrar em Campanha", style=discord.ButtonStyle.secondary)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message("[Acessível] Em breve: painel para entrar em campanha.", ephemeral=True)

# Exemplo de comando de campanha (adicione outros conforme necessário)
@campanha_group.command(name="listar", description="Lista as campanhas do usuário.")
async def campanha_listar(interaction: Interaction):
    campanhas = listar_campanhas(str(interaction.user.id))
    if not campanhas:
        await interaction.response.send_message("[Acessível] Você não participa de nenhuma campanha.", ephemeral=True)
        return
    msg = "\n".join([f"{nome}: {descricao or '(Sem descrição)'}" for camp_id, nome, descricao in campanhas])
    await interaction.response.send_message(f"Campanhas:\n{msg}", ephemeral=True)

# Adicione aqui outros comandos do grupo campanha conforme necessário.
