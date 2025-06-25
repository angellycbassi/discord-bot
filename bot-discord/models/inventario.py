from discord import app_commands, Interaction
import discord
from database import listar_inventario

inventario_group = app_commands.Group(name="inventario", description="Gerencie o inventário de fichas")

@inventario_group.command(name="painel", description="Abre o painel interativo de inventário.")
async def inventario_painel(interaction: Interaction):
    await interaction.response.send_message(
        "[Acessível] Painel de inventário:",
        view=InventarioPainelView(interaction.user.id),
        ephemeral=True
    )

class InventarioPainelView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.add_item(ListarInventarioButton(user_id))
        self.add_item(AdicionarItemButton(user_id))
        self.add_item(RemoverItemButton(user_id))

class ListarInventarioButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Listar Inventário", style=discord.ButtonStyle.primary)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        itens = listar_inventario(1)  # Exemplo: ficha_id=1
        if not itens:
            await interaction.response.send_message("[Acessível] Inventário vazio.", ephemeral=True)
            return
        msg = "\n".join([f"{item} (x{quantidade}) - {categoria}: {descricao}" for item, categoria, quantidade, descricao in itens])
        await interaction.response.send_message(f"Itens:\n{msg}", ephemeral=True)

class AdicionarItemButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Adicionar Item", style=discord.ButtonStyle.success)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message("[Acessível] Em breve: painel de adição de item.", ephemeral=True)

class RemoverItemButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Remover Item", style=discord.ButtonStyle.danger)
        self.user_id = user_id
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message("[Acessível] Em breve: painel de remoção de item.", ephemeral=True)

# Exemplo de comando de inventário (adicione outros conforme necessário)
@inventario_group.command(name="listar", description="Lista o inventário de uma ficha.")
@app_commands.describe(ficha_id="ID da ficha para listar o inventário")
async def inventario_listar(interaction: Interaction, ficha_id: int):
    itens = listar_inventario(ficha_id)
    if not itens:
        await interaction.response.send_message("[Acessível] Inventário vazio.", ephemeral=True)
        return
    msg = "\n".join([f"{item} (x{quantidade}) - {categoria}: {descricao}" for item, categoria, quantidade, descricao in itens])
    await interaction.response.send_message(f"Itens:\n{msg}", ephemeral=True)

# Adicione aqui outros comandos do grupo inventario conforme necessário.
