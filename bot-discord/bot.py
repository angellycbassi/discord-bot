"""
Main bot file for the Discord RPG Bot.
Handles bot initialization, cog loading, and logging configuration.
"""

import os
import logging
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, COMMAND_PREFIX
from database import init_db, criar_personagem, listar_personagens, listar_inventario, listar_campanhas, get_personagem_por_usuario, atualizar_posicao_personagem, set_avatar_personagem, get_avatar_personagem
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('discord_rpg_bot')

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Limites e eventos do mapa visual
MAPA_LIMITE_X = 9
MAPA_LIMITE_Y = 9
MAPA_EVENTOS = {
    (0, 0): "Você está no ponto inicial da aventura!",
    (5, 5): "⚡ Um portal mágico aparece! O que será que há além?",
    (9, 9): "🏰 Você avista um castelo lendário ao longe!"
}

# Grupos globais de slash commands
personagem_group = app_commands.Group(name="personagem", description="Gerencie fichas de personagem")
inventario_group = app_commands.Group(name="inventario", description="Gerencie o inventário de fichas")
combate_group = app_commands.Group(name="combate", description="Gerencie combates e ações de batalha")
campanha_group = app_commands.Group(name="campanha", description="Gerencie campanhas de RPG")
missao_group = app_commands.Group(name="missao", description="Gerencie missões e eventos")
aventura_group = app_commands.Group(name="aventura", description="Comandos de aventura de mundo aberto")
ia_group = app_commands.Group(name="ia", description="Comandos de integração com IA/NPCs")
economia_group = app_commands.Group(name="economia", description="Comandos de economia e loja")
engajamento_group = app_commands.Group(name="engajamento", description="Comandos de engajamento e gamificação")
idioma_group = app_commands.Group(name="idioma", description="Comandos de idioma e tradução")
visual_group = app_commands.Group(name="visual", description="Comandos de personalização visual")
relatorio_group = app_commands.Group(name="relatorio", description="Comandos de relatórios e estatísticas")
integracao_group = app_commands.Group(name="integracao", description="Comandos de integração externa")
monetizacao_group = app_commands.Group(name="monetizacao", description="Comandos de monetização e SaaS")
admin_group = app_commands.Group(name="admin", description="Comandos administrativos do bot")

# Lista de cogs padrão e avançados para carregamento automático
COGS = [
    'cogs.character_advanced',
    'cogs.inventory_advanced',
    'cogs.combat_advanced',
    'cogs.campaign',
    'cogs.quest_event',
    'cogs.ai_integration',
    'cogs.master_panel',
    'cogs.economy',
    'cogs.engagement',
    'cogs.multilang',
    'cogs.visuals',
    'cogs.reporting',
    'cogs.external_integration',
    'cogs.monetization',
    'cogs.open_world',
    # Adicione outros cogs personalizados aqui
]

@bot.event
async def on_ready():
    """
    Called when the bot is ready and connected to Discord.
    """
    init_db()  # Inicializa o banco de dados
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f'Bot online como: {bot.user} (ID: {bot.user.id})')
    
    # Load cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logger.info(f'Loaded cog: {cog}')
            print(f'Cog carregado: {cog}')
        except Exception as e:
            logger.error(f'Failed to load cog {cog}: {str(e)}')
            print(f'Erro ao carregar cog {cog}: {str(e)}')
    
    # Registrar grupos globais de slash commands
    bot.tree.add_command(personagem_group)
    bot.tree.add_command(inventario_group)
    bot.tree.add_command(combate_group)
    bot.tree.add_command(campanha_group)
    bot.tree.add_command(missao_group)
    bot.tree.add_command(aventura_group)
    bot.tree.add_command(ia_group)
    bot.tree.add_command(economia_group)
    bot.tree.add_command(engajamento_group)
    bot.tree.add_command(idioma_group)
    bot.tree.add_command(visual_group)
    bot.tree.add_command(relatorio_group)
    bot.tree.add_command(integracao_group)
    bot.tree.add_command(monetizacao_group)
    bot.tree.add_command(admin_group)

    print('Sincronizando comandos globais...')
    try:
        await bot.tree.sync()
        logger.info('Comandos globais ressincronizados!')
        print('Comandos slash sincronizados com sucesso!')
        print('Comandos disponíveis:')
        for cmd in bot.tree.get_commands():
            print(f'- /{cmd.name}: {cmd.description}')
    except Exception as e:
        logger.error(f'Erro ao sincronizar comandos: {str(e)}')
        print(f'Erro ao sincronizar comandos: {str(e)}')
    print("Comandos globais sincronizados!")

@bot.event
async def on_command_error(ctx, error):
    """
    Global error handler for commands.
    """
    if isinstance(error, commands.CommandNotFound):
        return
    
    logger.error(f'Error in {ctx.command}: {str(error)}')
    await ctx.send(f'An error occurred: {str(error)}')

@bot.tree.command(name="help", description="Mostra todos os comandos disponíveis e exemplos de uso.")
async def help_command(interaction: discord.Interaction):
    help_text = (
        "[Acessível]\n"
        "**Painel Interativo:**\n"
        "Use `/painel` para abrir o painel visual do bot.\n"
        "\n**Personagem:**\n"
        "/personagem criar <nome> [template] — Cria ficha\n"
        "/personagem listar — Lista fichas\n"
        "/personagem editar <ficha_id> <campo> <valor> — Edita ficha\n"
        "/personagem remover <ficha_id> — Remove ficha\n"
        "/personagem template <ação> <nome> — Gerencia templates\n"
        "\n**Inventário:**\n"
        "/inventario adicionar <ficha_id> <item> <categoria> [peso] [descrição]\n"
        "/inventario remover <ficha_id> <item_id>\n"
        "/inventario listar <ficha_id>\n"
        "/inventario editar <ficha_id> <item_id> <campo> <valor>\n"
        "\n**Combate:**\n"
        "/combate iniciar <campanha_id> [descrição]\n"
        "/combate atacar <combate_id> <alvo> [macro]\n"
        "/combate defender <combate_id>\n"
        "/combate usar_item <combate_id> <item_id>\n"
        "/combate log <combate_id>\n"
        "\n**Campanha:**\n"
        "/campanha criar <nome>\n"
        "/campanha convidar <campanha_id> <usuário>\n"
        "/campanha registrar_sessao <campanha_id> [descrição]\n"
        "/campanha xp <campanha_id> <usuário> <quantidade>\n"
        "\n**Missão/Eventos:**\n"
        "/missao criar <nome> [recompensa]\n"
        "/missao progresso <missao_id> <progresso>\n"
        "/missao sortear <evento_id>\n"
        "\n**Aventura de Mundo Aberto:**\n"
        "/aventura iniciar [solo]\n"
        "/aventura convidar <usuário>\n"
        "/aventura mapa\n"
        "/aventura boss\n"
        "\n**IA/NPCs:**\n"
        "/ia npc <nome> <mensagem>\n"
        "/ia sugerir_evento <campanha_id>\n"
        "\n**Economia/Loja:**\n"
        "/economia transferir <usuário> <quantidade>\n"
        "/economia loja\n"
        "\n**Engajamento/Gamificação:**\n"
        "/engajamento ranking\n"
        "/engajamento desafio\n"
        "\n**Idioma/Tradução:**\n"
        "/idioma definir <idioma>\n"
        "\n**Visual/Temas:**\n"
        "/visual tema <tema>\n"
        "\n**Relatórios:**\n"
        "/relatorio exportar [tipo]\n"
        "\n**Integração Externa:**\n"
        "/integracao google_sheets\n"
        "\n**Monetização:**\n"
        "/monetizacao plano\n"
        "\n\nDica: Use os botões e comandos sempre que possível. Todas as funções possuem suporte a leitores de tela e tooltips detalhados."
    )
    await interaction.response.send_message(help_text, ephemeral=True)

from database import listar_personagens, listar_inventario, listar_campanhas

# Temas visuais disponíveis
THEMES = {
    "dark": {
        "color": discord.Color.dark_grey(),
        "footer": "Modo Noturno Ativo",
        "icon": "🌑"
    },
    "medieval": {
        "color": discord.Color.gold(),
        "footer": "Era Medieval",
        "icon": "🛡️"
    },
    "cyberpunk": {
        "color": discord.Color.teal(),
        "footer": "Cyberpunk Style",
        "icon": "🤖"
    },
    "classic": {
        "color": discord.Color.blue(),
        "footer": "Clássico RPGium",
        "icon": "🎲"
    }
}

# Banco de dados: tema e avatar por usuário (exemplo simples, ideal: mover para database.py)
user_visual_settings = {}

def set_user_theme(user_id, theme):
    user_visual_settings[str(user_id)] = user_visual_settings.get(str(user_id), {})
    user_visual_settings[str(user_id)]["theme"] = theme

def get_user_theme(user_id):
    return user_visual_settings.get(str(user_id), {}).get("theme", "classic")

def set_user_avatar(user_id, url):
    user_visual_settings[str(user_id)] = user_visual_settings.get(str(user_id), {})
    user_visual_settings[str(user_id)]["avatar"] = url

def get_user_avatar(user_id):
    return user_visual_settings.get(str(user_id), {}).get("avatar", None)

# Utilitário para gerar embed temático
def gerar_embed_tema(user_id, title, description, fields=None):
    theme = get_user_theme(user_id)
    theme_data = THEMES.get(theme, THEMES["classic"])
    # Adiciona prefixo para leitores de tela
    description = f"[Acessível] {description}"
    embed = discord.Embed(
        title=f"{theme_data['icon']} {title}",
        description=description,
        color=theme_data["color"]
    )
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    embed.set_footer(text=theme_data["footer"])
    avatar_url = get_user_avatar(user_id)
    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
    return embed

# Comando para escolher tema visual
@visual_group.command(name="tema", description="Escolha o tema visual do seu painel e fichas.")
@app_commands.describe(tema="Escolha entre: dark, medieval, cyberpunk, classic")
async def escolher_tema(interaction: discord.Interaction, tema: str):
    tema = tema.lower()
    if tema not in THEMES:
        await interaction.response.send_message(f"Temas disponíveis: {', '.join(THEMES.keys())}", ephemeral=True)
        return
    set_user_theme(interaction.user.id, tema)
    embed = gerar_embed_tema(interaction.user.id, "Tema Atualizado", f"Seu tema foi alterado para **{tema}**!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Modal para upload de avatar customizado
class AvatarModal(discord.ui.Modal, title="Avatar do Personagem"):
    url = discord.ui.TextInput(label="URL da Imagem do Avatar", placeholder="Cole o link da imagem (jpg/png)", max_length=200)
    async def on_submit(self, interaction: discord.Interaction):
        set_user_avatar(interaction.user.id, self.url.value)
        embed = gerar_embed_tema(interaction.user.id, "Avatar Atualizado", "Seu avatar foi salvo! Ele aparecerá nas fichas e painéis.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Botão para abrir modal de avatar
class AvatarButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Avatar", style=discord.ButtonStyle.secondary, custom_id="avatar_btn")
        self.user_id = user_id
        self.tooltip = "Clique para definir ou atualizar seu avatar personalizado. O avatar será exibido em todas as suas fichas e painéis. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AvatarModal())

# Exemplo de uso do embed temático e botão de avatar no painel do jogador
class PainelJogadorView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.atualizar_fichas()
        self.add_item(AvatarButton(self.user_id))
    def atualizar_fichas(self):
        self.clear_items()
        fichas = listar_personagens(str(self.user_id))
        if not fichas:
            self.add_item(CriarFichaButton())
        else:
            for idx, (nome, raca, classe, xp, nivel, status) in enumerate(fichas, 1):
                self.add_item(FichaButton(idx, nome, raca, classe, xp, nivel, status, self.user_id))
            self.add_item(CriarFichaButton())
        self.add_item(VerInventarioButton(self.user_id))
        self.add_item(VerCampanhasButton(self.user_id))
        self.add_item(VerMapaButton(self.user_id))
        self.add_item(CombateButton(self.user_id))
        # Tooltips detalhados para acessibilidade
        for item in self.children:
            if hasattr(item, 'tooltip'):
                item.label = f"{item.label} ℹ️"
                item.emoji = "ℹ️"

class CriarFichaButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Criar Ficha", style=discord.ButtonStyle.success)
        self.tooltip = "Crie uma nova ficha de personagem para começar sua aventura. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("[Acessível] Use o comando `/personagem criar <nome>` para criar sua ficha. Caso precise de ajuda, utilize `/help`.", ephemeral=True)

class FichaButton(discord.ui.Button):
    def __init__(self, idx, nome, raca, classe, xp, nivel, status, user_id):
        super().__init__(label=f"{idx}. {nome}", style=discord.ButtonStyle.primary)
        self.idx = idx
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.xp = xp
        self.nivel = nivel
        self.status = status
        self.user_id = user_id
        self.tooltip = f"Clique para ver detalhes completos da ficha de {nome}. Raça: {raca}, Classe: {classe}, XP: {xp}, Nível: {nivel}, Status: {status}. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        fichas = listar_personagens(str(self.user_id))
        personagem = fichas[self.idx - 1]
        embed = gerar_embed_ficha_personagem(self.user_id, self.idx, personagem)
        embed.description += "\n\n[Acessível] Dica: Use os botões abaixo para acessar inventário, campanhas, mapa e combate."
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VerInventarioButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Ver Inventário", style=discord.ButtonStyle.secondary)
        self.user_id = user_id
        self.tooltip = "Visualize o inventário do seu personagem principal. Cada item é exibido com nome, categoria e descrição detalhada. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        fichas = listar_personagens(str(self.user_id))
        if not fichas:
            await interaction.response.send_message("[Acessível] Você não possui fichas para consultar inventário.", ephemeral=True)
            return
        personagem_id = 1
        itens = listar_inventario(personagem_id)
        if not itens:
            await interaction.response.send_message("[Acessível] Inventário vazio.", ephemeral=True)
            return
        fields = [(f"{item} (x{quantidade})", f"Categoria: {categoria}\n{descricao}", False) for item, categoria, quantidade, descricao in itens]
        embed = gerar_embed_tema(self.user_id, "Inventário do Herói", "Itens encontrados em sua jornada. Use comandos de inventário para adicionar, remover ou editar itens. [Acessível]", fields)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VerCampanhasButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Ver Campanhas", style=discord.ButtonStyle.success)
        self.user_id = user_id
        self.tooltip = "Veja as campanhas das quais você participa. Cada campanha mostra nome e descrição detalhada. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        campanhas = listar_campanhas(str(self.user_id))
        if not campanhas:
            await interaction.response.send_message("[Acessível] Você não participa de nenhuma campanha.", ephemeral=True)
            return
        fields = [(nome, descricao or "(Sem descrição)", False) for camp_id, nome, descricao in campanhas]
        embed = gerar_embed_tema(self.user_id, "Campanhas Ativas", "Suas campanhas em andamento. Use comandos de campanha para gerenciar sessões, XP e convites. [Acessível]", fields)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VerMapaButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Mapa", style=discord.ButtonStyle.primary)
        self.user_id = user_id
        self.tooltip = "Visualize o mapa do mundo e mova seu personagem. O mapa é exibido em formato visual e texto para leitores de tela. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        from database import get_personagem_por_usuario, listar_personagens
        fichas = listar_personagens(str(self.user_id))
        if not fichas:
            await interaction.response.send_message("[Acessível] Nenhum personagem encontrado.", ephemeral=True)
            return
        if len(fichas) == 1:
            personagem = get_personagem_por_usuario(str(self.user_id))
            pid, nome, pos = personagem
            x, y = map(int, pos.split(","))
            evento = MAPA_EVENTOS.get((x, y))
            embed = gerar_embed_mapa(nome, x, y, evento)
            embed.description += "\n\n[Acessível] Dica: Use os botões de direção para mover seu personagem. O mapa é acessível para leitores de tela."
            file = discord.File("data/mapa_rpgium.png", filename="mapa_rpgium.png")
            await interaction.response.send_message(embed=embed, view=MapaView(pid, pos), file=file, ephemeral=True)
        else:
            await interaction.response.send_message("[Acessível] Selecione o personagem para visualizar o mapa.", view=SelecionarPersonagemView(self.user_id), ephemeral=True)

class CombateButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Combate", style=discord.ButtonStyle.danger)
        self.user_id = user_id
        self.tooltip = "Inicie um combate épico com seus personagens. O combate é exibido em formato visual e texto detalhado para leitores de tela. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        fichas = listar_personagens(str(self.user_id))
        if not fichas:
            await interaction.response.send_message("[Acessível] Crie uma ficha antes de iniciar um combate!", ephemeral=True)
            return
        await interaction.response.send_modal(IniciarCombateModalAvancado(self.user_id, fichas))

# Melhorar alto contraste: tema acessível já está disponível como 'dark', mas pode ser expandido para 'acessibilidade' se desejar.
@visual_group.command(name="contraste", description="Ativa/desativa modo de alto contraste para acessibilidade.")
async def toggle_contraste(interaction: discord.Interaction):
    atual = get_user_theme(interaction.user.id)
    if atual != "dark":
        set_user_theme(interaction.user.id, "dark")
        msg = "Alto contraste ativado (tema escuro e acessível)."
    else:
        set_user_theme(interaction.user.id, "classic")
        msg = "Alto contraste desativado."
    embed = gerar_embed_tema(interaction.user.id, "Acessibilidade", msg)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Garantir textos claros para leitores de tela nos principais embeds
def gerar_embed_tema(user_id, title, description, fields=None):
    theme = get_user_theme(user_id)
    theme_data = THEMES.get(theme, THEMES["classic"])
    # Adiciona prefixo para leitores de tela
    description = f"[Acessível] {description}"
    embed = discord.Embed(
        title=f"{theme_data['icon']} {title}",
        description=description,
        color=theme_data["color"]
    )
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
    embed.set_footer(text=theme_data["footer"])
    avatar_url = get_user_avatar(user_id)
    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
    return embed

@bot.event
async def on_guild_join(guild):
    # Envia painel automático ao entrar em um novo servidor
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            try:
                await channel.send("Olá! Use o painel abaixo para acessar as funções do bot:", view=PainelView())
            except Exception:
                pass
            break

#@admin_group.command(name="limpar_banco", description="Remove todos os dados do banco de dados do bot (apenas para o owner)")
#async def limpar_banco_cmd(interaction: discord.Interaction):
#    if interaction.user.id != bot.owner_id:
#        await interaction.response.send_message("[Acessível] ❌ Apenas o proprietário do bot pode executar este comando!", ephemeral=True)
#        return
#    try:
#        limpar_banco()
#        await interaction.response.send_message("[Acessível] ✅ Banco de dados limpo com sucesso! Todas as informações foram removidas.", ephemeral=True)
#    except Exception as e:
#        await interaction.response.send_message(f"[Acessível] ❌ Erro ao limpar banco: {str(e)}", ephemeral=True)

@admin_group.command(name="sync", description="Força a sincronização dos comandos do bot (apenas para o owner)")
async def sync_commands(interaction: discord.Interaction):
    if interaction.user.id != bot.owner_id:
        await interaction.response.send_message("[Acessível] ❌ Apenas o proprietário do bot pode executar este comando!", ephemeral=True)
        return
    try:
        print("Iniciando limpeza e sincronização forçada...")
        await bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        print("Comandos limpos, registrando novos comandos...")
        bot.tree.add_command(personagem_group)
        bot.tree.add_command(inventario_group)
        bot.tree.add_command(combate_group)
        bot.tree.add_command(campanha_group)
        bot.tree.add_command(missao_group)
        bot.tree.add_command(aventura_group)
        bot.tree.add_command(ia_group)
        bot.tree.add_command(economia_group)
        bot.tree.add_command(engajamento_group)
        bot.tree.add_command(idioma_group)
        bot.tree.add_command(visual_group)
        bot.tree.add_command(relatorio_group)
        bot.tree.add_command(integracao_group)
        bot.tree.add_command(monetizacao_group)
        bot.tree.add_command(admin_group)
        await bot.tree.sync()
        await interaction.response.send_message("[Acessível] ✅ Comandos sincronizados com sucesso! Todos os comandos slash estão atualizados.", ephemeral=True)
        print("Sincronização forçada concluída!")
        print('Comandos disponíveis após sync:')
        for cmd in bot.tree.get_commands():
            print(f'- /{cmd.name}: {cmd.description}')
    except Exception as e:
        await interaction.response.send_message(f"[Acessível] ❌ Erro ao sincronizar: {str(e)}", ephemeral=True)
        print(f"Erro durante sincronização: {str(e)}")

# Exemplo de subcomando para o grupo aventura
@aventura_group.command(name="iniciar", description="Inicia uma aventura de mundo aberto.")
async def aventura_iniciar(interaction: discord.Interaction):
    await interaction.response.send_message("🌄 Uma nova aventura começou! Prepare-se para explorar o desconhecido.", ephemeral=True)

# Handler para chamada direta ao grupo /aventura
@aventura_group.command(name="_placeholder", description="Mostra informações sobre o grupo de aventura.")
async def aventura_placeholder(interaction: discord.Interaction):
    await interaction.response.send_message("Use um subcomando, como `/aventura iniciar`, para começar sua jornada!", ephemeral=True)

class CombateButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="Combate", style=discord.ButtonStyle.danger)
        self.user_id = user_id
    async def callback(self, interaction: discord.Interaction):
        fichas = listar_personagens(str(self.user_id))
        if not fichas:
            await interaction.response.send_message("Crie uma ficha antes de iniciar um combate!", ephemeral=True)
            return
        await interaction.response.send_modal(IniciarCombateModalAvancado(self.user_id, fichas))

class IniciarCombateModalAvancado(discord.ui.Modal, title="Iniciar Combate Avançado"):
    def __init__(self, user_id, fichas):
        super().__init__()
        self.user_id = user_id
        self.fichas = fichas
        nomes = ", ".join([f[0] for f in fichas])
        self.personagens = discord.ui.TextInput(label="Seus personagens (separe por vírgula)", placeholder=f"Ex: {nomes}", max_length=100)
        self.inimigos = discord.ui.TextInput(label="Inimigos (separe por vírgula)", placeholder="Ex: Goblin, Orc, Dragão", max_length=100)
        self.add_item(self.personagens)
        self.add_item(self.inimigos)
    async def on_submit(self, interaction: discord.Interaction):
        nomes_personagens = [n.strip() for n in self.personagens.value.split(",") if n.strip()]
        nomes_inimigos = [n.strip() for n in self.inimigos.value.split(",") if n.strip()]
        hp_personagens = {nome: 100 for nome in nomes_personagens}
        hp_inimigos = {nome: random.randint(40, 120) for nome in nomes_inimigos}
        embed = gerar_embed_combate_grupo(hp_personagens, hp_inimigos)
        await interaction.response.send_message(embed=embed, view=CombateGrupoView(hp_personagens, hp_inimigos, self.user_id), ephemeral=True)

def gerar_embed_combate_grupo(hp_personagens, hp_inimigos, acao=None, destaque=None):
    def barra(hp, max_hp=100):
        blocos = int(hp / max_hp * 10)
        return "🟩" * blocos + "⬜" * (10 - blocos)
    desc = "**Aventureiros:**\n"
    for nome, hp in hp_personagens.items():
        desc += f"{nome}: {barra(hp)} {hp}/100\n"
    desc += "\n**Inimigos:**\n"
    for nome, hp in hp_inimigos.items():
        desc += f"{nome}: {barra(hp, 120)} {hp}/120\n"
    if acao:
        desc += f"\n**Ação:** {acao}"
    if destaque:
        desc += f"\n{destaque}"
    embed = discord.Embed(
        title="⚔️ Combate em Grupo!",
        description=desc,
        color=discord.Color.red()
    )
    embed.set_footer(text="Escolha uma ação para cada personagem!")
    return embed

class CombateGrupoView(discord.ui.View):
    def __init__(self, hp_personagens, hp_inimigos, user_id):
        super().__init__(timeout=90)
        self.hp_personagens = hp_personagens
        self.hp_inimigos = hp_inimigos
        self.user_id = user_id
        self.log = []
        for nome in hp_personagens:
            self.add_item(AcaoPersonagemButton(nome, self))
        self.add_item(ExportarLogButton(self))

class ExportarLogButton(discord.ui.Button):
    def __init__(self, combate_view):
        super().__init__(label="Exportar Log", style=discord.ButtonStyle.secondary)
        self.combate_view = combate_view
    async def callback(self, interaction: discord.Interaction):
        log_text = "\n".join(self.combate_view.log) or "Nenhuma ação registrada."
        with open("log_combate.txt", "w", encoding="utf-8") as f:
            f.write(log_text)
        file = discord.File("log_combate.txt", filename="log_combate.txt")
        await interaction.response.send_message("Log do combate exportado:", file=file, ephemeral=True)

class AcaoPersonagemButton(discord.ui.Button):
    def __init__(self, nome, combate_view):
        super().__init__(label=f"Ação: {nome}", style=discord.ButtonStyle.primary)
        self.nome = nome
        self.combate_view = combate_view
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AcaoModal(self.nome, self.combate_view))

class AcaoModal(discord.ui.Modal, title="Escolha sua ação"):
    def __init__(self, nome, combate_view):
        super().__init__()
        self.nome = nome
        self.combate_view = combate_view
        self.acao = discord.ui.TextInput(label="Ação (atacar <inimigo>, defender, usar item, fugir, habilidade <nome>)", max_length=50)
        self.add_item(self.acao)
    async def on_submit(self, interaction: discord.Interaction):
        acao = self.acao.value.lower()
        destaque = None
        log = []
        # Habilidades únicas por personagem
        habilidades_personagem = ["ataque duplo", "cura em grupo", "escudo mágico"]
        if self.nome.lower() == "grommash":
            habilidades_personagem.append("fúria")
        if self.nome.lower() == "elora":
            habilidades_personagem.append("regeneração")
        if acao.startswith("habilidade"):
            partes = acao.split()
            if len(partes) > 1:
                hab = " ".join(partes[1:])
                if hab not in habilidades_personagem:
                    destaque = f"❌ {self.nome} não possui a habilidade '{hab}'."
                    log.append(destaque)
                elif hab == "ataque duplo":
                    if len(self.combate_view.hp_inimigos) > 1:
                        destaque = "❌ Ataque Duplo só pode ser usado contra um inimigo."
                        log.append(destaque)
                    else:
                        alvo = list(self.combate_view.hp_inimigos.keys())[0]
                        dano1 = random.randint(8, 18)
                        dano2 = random.randint(8, 18)
                        self.combate_view.hp_inimigos[alvo] -= (dano1 + dano2)
                        destaque = f"⚡ {self.nome} usou Ataque Duplo em {alvo} causando {dano1+dano2} de dano!"
                        log.append(destaque)
                        if self.combate_view.hp_inimigos[alvo] <= 0:
                            destaque += f"\n💀 {alvo} foi derrotado!"
                            del self.combate_view.hp_inimigos[alvo]
                elif hab == "cura em grupo":
                    for p in self.combate_view.hp_personagens:
                        self.combate_view.hp_personagens[p] = min(100, self.combate_view.hp_personagens[p] + 20)
                    destaque = f"✨ {self.nome} usou Cura em Grupo! Todos recuperam 20 HP."
                    log.append(destaque)
                elif hab == "escudo mágico":
                    destaque = f"🛡️ {self.nome} conjurou Escudo Mágico! Dano recebido será reduzido."
                    log.append(destaque)
        # Ações padrão
        if acao.startswith("atacar"):
            partes = acao.split()
            if len(partes) > 1:
                alvo = partes[1]
                if alvo in self.combate_view.hp_inimigos:
                    dano = random.randint(10, 30)
                    self.combate_view.hp_inimigos[alvo] -= dano
                    destaque = f"🗡️ {self.nome} atacou {alvo} causando {dano} de dano!"
                    log.append(destaque)
                    if self.combate_view.hp_inimigos[alvo] <= 0:
                        destaque += f"\n💀 {alvo} foi derrotado!"
                        del self.combate_view.hp_inimigos[alvo]
        elif acao == "defender":
            destaque = f"🛡️ {self.nome} está em posição defensiva!"
            log.append(destaque)
        elif acao == "usar item":
            cura = random.randint(15, 30)
            self.combate_view.hp_personagens[self.nome] = min(100, self.combate_view.hp_personagens[self.nome] + cura)
            destaque = f"💊 {self.nome} usou um item e recuperou {cura} de HP!"
            log.append(destaque)
        elif acao == "fugir":
            destaque = f"🏃 {self.nome} fugiu do combate!"
            log.append(destaque)
            del self.combate_view.hp_personagens[self.nome]
        # Inimigos com poderes únicos
        for inimigo in list(self.combate_view.hp_inimigos.keys()):
            poder = PODERES_INIMIGOS.get(inimigo, None)
            if poder and random.random() < 0.4:
                if poder == "fúria":
                    dano = random.randint(20, 40)
                    alvo = random.choice(list(self.combate_view.hp_personagens.keys()))
                    self.combate_view.hp_personagens[alvo] -= dano
                    log.append(f"💢 {inimigo} entrou em Fúria e causou {dano} de dano em {alvo}!")
                elif poder == "chama mortal":
                    dano = random.randint(25, 50)
                    alvo = random.choice(list(self.combate_view.hp_personagens.keys()))
                    self.combate_view.hp_personagens[alvo] -= dano
                    log.append(f"🔥 {inimigo} usou Chama Mortal em {alvo} causando {dano} de dano!")
                elif poder == "regeneração":
                    self.combate_view.hp_inimigos[inimigo] = min(120, self.combate_view.hp_inimigos[inimigo] + 20)
                    log.append(f"✨ {inimigo} regenerou 20 HP!")
                elif poder == "maldição":
                    alvo = random.choice(list(self.combate_view.hp_personagens.keys()))
                    log.append(f"🕸️ {inimigo} lançou Maldição em {alvo}! Próximo ataque dele será reduzido.")
        # Salva log
        self.combate_view.log.extend(log)
        # Checa fim do combate
        if not self.combate_view.hp_inimigos:
            await interaction.response.edit_message(embed=gerar_embed_vitoria_grupo(self.combate_view.hp_personagens, self.combate_view.user_id, log), view=None)
            return
        if not self.combate_view.hp_personagens:
            embed = discord.Embed(title="Derrota!", description="Todos os aventureiros caíram ou fugiram.", color=discord.Color.dark_grey())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        embed = gerar_embed_combate_grupo(self.combate_view.hp_personagens, self.combate_view.hp_inimigos, acao=self.acao.value, destaque="\n".join(log))
        await interaction.response.edit_message(embed=embed, view=self.combate_view)

def gerar_embed_vitoria_grupo(hp_personagens, user_id, log=None):
    # Loot aleatório para cada personagem
    loots = [random.choice(["Poção de Vida", "Espada Curta", "Elixir", "Moeda de Ouro"]) for _ in hp_personagens]
    xps = [random.randint(20, 50) for _ in hp_personagens]
    fichas = listar_personagens(str(user_id))
    from database import adicionar_item, adicionar_xp
    for idx, (nome, *_rest) in enumerate(fichas):
        if idx < len(loots):
            adicionar_item(idx+1, loots[idx], "Loot", 0, "Item de combate.", 1)
            adicionar_xp(str(user_id), idx+1, xps[idx])
    desc = ""
    for i, nome in enumerate(hp_personagens):
        desc += f"{nome}: +{xps[i]} XP, loot: {loots[i]}\n"
    if log:
        desc += "\n**Log do Combate:**\n" + "\n".join(log)
    embed = discord.Embed(
        title="🎉 Vitória do Grupo!",
        description=f"Todos os inimigos foram derrotados!\n\n{desc}",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Itens e XP distribuídos entre os personagens sobreviventes!")
    return embed

# PvP: comando para desafiar outro usuário
@bot.tree.command(name="pvp", description="Desafie outro jogador para um combate PvP!")
@app_commands.describe(oponente="Mencione o usuário a ser desafiado")
async def pvp_command(interaction: discord.Interaction, oponente: discord.Member):
    fichas1 = listar_personagens(str(interaction.user.id))
    fichas2 = listar_personagens(str(oponente.id))
    if not fichas1 or not fichas2:
        await interaction.response.send_message("Ambos os jogadores precisam ter pelo menos uma ficha!", ephemeral=True)
        return
    nomes1 = [f[0] for f in fichas1]
    nomes2 = [f[0] for f in fichas2]
    hp1 = {nome: 100 for nome in nomes1}
    hp2 = {nome: 100 for nome in nomes2}
    embed = discord.Embed(
        title="⚔️ PvP: Combate entre Jogadores!",
        description=f"{interaction.user.mention} vs {oponente.mention}\nCada jogador pode agir com seus personagens.",
        color=discord.Color.purple()
    )
    embed.add_field(name="Aventureiros 1", value=", ".join(nomes1), inline=True)
    embed.add_field(name="Aventureiros 2", value=", ".join(nomes2), inline=True)
    await interaction.response.send_message(embed=embed, view=PvPView(hp1, hp2, interaction.user.id, oponente.id), ephemeral=True)

class PvPView(discord.ui.View):
    def __init__(self, hp1, hp2, user1_id, user2_id):
        super().__init__(timeout=120)
        self.hp1 = hp1
        self.hp2 = hp2
        self.user1_id = user1_id
        self.user2_id = user2_id
        for nome in hp1:
            self.add_item(PvPAcaoButton(nome, 1, self))
        for nome in hp2:
            self.add_item(PvPAcaoButton(nome, 2, self))

class PvPAcaoButton(discord.ui.Button):
    def __init__(self, nome, grupo, pvp_view):
        super().__init__(label=f"Ação: {nome}", style=discord.ButtonStyle.primary)
        self.nome = nome
        self.grupo = grupo
        self.pvp_view = pvp_view
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(PvPAcaoModal(self.nome, self.grupo, self.pvp_view))

class PvPAcaoModal(discord.ui.Modal, title="Ação PvP"):
    def __init__(self, nome, grupo, pvp_view):
        super().__init__()
        self.nome = nome
        self.grupo = grupo
        self.pvp_view = pvp_view
        self.acao = discord.ui.TextInput(label="Ação (atacar <alvo>, defender, usar item, fugir, habilidade <nome>)", max_length=50)
        self.add_item(self.acao)
    async def on_submit(self, interaction: discord.Interaction):
        acao = self.acao.value.lower()
        log = []
        if self.grupo == 1:
            hp_aliados = self.pvp_view.hp1
            hp_inimigos = self.pvp_view.hp2
        else:
            hp_aliados = self.pvp_view.hp2
            hp_inimigos = self.pvp_view.hp1
        if acao.startswith("atacar"):
            partes = acao.split()
            if len(partes) > 1:
                alvo = partes[1]
                if alvo in hp_inimigos:
                    dano = random.randint(10, 30)
                    hp_inimigos[alvo] -= dano
                    log.append(f"🗡️ {self.nome} atacou {alvo} causando {dano} de dano!")
                    if hp_inimigos[alvo] <= 0:
                        log.append(f"💀 {alvo} foi derrotado!")
                        del hp_inimigos[alvo]
        elif acao == "defender":
            log.append(f"🛡️ {self.nome} está em posição defensiva!")
        elif acao == "usar item":
            cura = random.randint(15, 30)
            hp_aliados[self.nome] = min(100, hp_aliados[self.nome] + cura)
            log.append(f"💊 {self.nome} usou um item e recuperou {cura} de HP!")
        elif acao == "fugir":
            log.append(f"🏃 {self.nome} fugiu do combate!")
            del hp_aliados[self.nome]
        elif acao.startswith("habilidade"):
            partes = acao.split()
            if len(partes) > 1:
                hab = " ".join(partes[1:])
                if hab == "ataque duplo":
                    alvos = list(hp_inimigos.keys())
                    if alvos:
                        alvo = alvos[0]
                        total_dano = 0
                        for _ in range(2):
                            dano = random.randint(8, 18)
                            hp_inimigos[alvo] -= dano
                            total_dano += dano
                        log.append(f"⚡ {self.nome} usou Ataque Duplo em {alvo} causando {total_dano} de dano!")
                        if hp_inimigos[alvo] <= 0:
                            log.append(f"💀 {alvo} foi derrotado!")
                            del hp_inimigos[alvo]
                elif hab == "cura em grupo":
                    for p in hp_aliados:
                        hp_aliados[p] = min(100, hp_aliados[p] + 20)
                    log.append(f"✨ {self.nome} usou Cura em Grupo! Todos recuperam 20 HP.")
                elif hab == "escudo mágico":
                    log.append(f"🛡️ {self.nome} conjurou Escudo Mágico! Dano recebido será reduzido.")
        # Checa fim do PvP
        if not hp_inimigos:
            embed = discord.Embed(title="🏆 Vitória no PvP!", description="Todos os personagens do adversário foram derrotados!", color=discord.Color.gold())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        if not hp_aliados:
            embed = discord.Embed(title="Derrota no PvP!", description="Todos os seus personagens caíram ou fugiram.", color=discord.Color.dark_grey())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        desc = "**Aliados:**\n" + ", ".join(f"{n}: {hp_aliados[n]} HP" for n in hp_aliados)
        desc += "\n**Inimigos:**\n" + ", ".join(f"{n}: {hp_inimigos[n]} HP" for n in hp_inimigos)
        desc += "\n\n" + "\n".join(log)
        embed = discord.Embed(title="⚔️ PvP em andamento", description=desc, color=discord.Color.purple())
        await interaction.response.edit_message(embed=embed, view=self.pvp_view)

# Habilidades especiais e poderes únicos
HABILIDADES = {
    "ataque duplo": "Ataca duas vezes o mesmo inimigo.",
    "cura em grupo": "Cura todos os aliados em 20 HP.",
    "escudo mágico": "Reduz o dano recebido pela metade no próximo turno.",
    "fúria": "Aumenta o dano do próximo ataque em 50%.",
    "regeneração": "Recupera 10 HP ao final de cada turno.",
    "maldição": "Reduz o ataque do inimigo pela metade por 2 turnos."
}

PODERES_INIMIGOS = {
    "Orc": "fúria",
    "Dragão": "chama mortal",
    "Lich": "maldição",
    "Troll": "regeneração"
}

from database import set_avatar_personagem, get_avatar_personagem

# Modal para upload de avatar customizado por personagem
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

# Comando para definir avatar de uma ficha
@personagem_group.command(name="avatar", description="Defina o avatar de uma ficha de personagem.")
@app_commands.describe(ficha_id="ID da ficha para definir o avatar")
async def personagem_avatar(interaction: discord.Interaction, ficha_id: int):
    fichas = listar_personagens(str(interaction.user.id))
    if not fichas or ficha_id < 1 or ficha_id > len(fichas):
        await interaction.response.send_message("Ficha não encontrada.", ephemeral=True)
        return
    await interaction.response.send_modal(AvatarPersonagemModal(ficha_id))

# Utilitário para gerar embed de ficha com avatar customizado
def gerar_embed_ficha_personagem(user_id, ficha_id, personagem):
    nome, raca, classe, xp, nivel, status = personagem
    avatar_url = get_avatar_personagem(ficha_id)
    embed = gerar_embed_tema(user_id, f"Ficha de {nome}", f"Raça: {raca}\nClasse: {classe}\nXP: {xp}\nNível: {nivel}\nStatus: {status}")
    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
    return embed

def gerar_embed_mapa(nome, x, y, evento=None):
    desc = f"[Acessível] Posição atual de {nome}: ({x}, {y})\n"
    if evento:
        desc += f"Evento: {evento}\n"
    desc += "Use os botões para mover seu personagem pelo mapa.\nO mapa visual está disponível como imagem anexa."
    embed = discord.Embed(
        title=f"🗺️ Mapa de {nome}",
        description=desc,
        color=discord.Color.green()
    )
    embed.set_footer(text="Movimente-se pelo mundo RPGium!")
    return embed

class MapaView(discord.ui.View):
    def __init__(self, personagem_id, pos):
        super().__init__(timeout=60)
        self.personagem_id = personagem_id
        self.x, self.y = map(int, pos.split(","))
        self.add_item(MoverButton("⬅️", -1, 0, self))
        self.add_item(MoverButton("➡️", 1, 0, self))
        self.add_item(MoverButton("⬆️", 0, -1, self))
        self.add_item(MoverButton("⬇️", 0, 1, self))
    async def atualizar_mapa(self, interaction):
        from database import atualizar_posicao_personagem, get_personagem_por_usuario
        if 0 <= self.x <= MAPA_LIMITE_X and 0 <= self.y <= MAPA_LIMITE_Y:
            atualizar_posicao_personagem(self.personagem_id, f"{self.x},{self.y}")
            personagem = get_personagem_por_usuario(str(interaction.user.id))
            pid, nome, pos = personagem
            x, y = map(int, pos.split(","))
            evento = MAPA_EVENTOS.get((x, y))
            embed = gerar_embed_mapa(nome, x, y, evento)
            file = discord.File("data/mapa_rpgium.png", filename="mapa_rpgium.png")
            await interaction.response.edit_message(embed=embed, view=self, file=file)
        else:
            await interaction.response.send_message("[Acessível] Limite do mapa atingido.", ephemeral=True)

class MoverButton(discord.ui.Button):
    def __init__(self, label, dx, dy, mapa_view):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.dx = dx
        self.dy = dy
        self.mapa_view = mapa_view
        self.tooltip = f"Mover {label} pelo mapa. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        self.mapa_view.x += self.dx
        self.mapa_view.y += self.dy
        await self.mapa_view.atualizar_mapa(interaction)

class SelecionarPersonagemView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=30)
        self.user_id = user_id
        fichas = listar_personagens(str(user_id))
        for idx, (nome, *_rest) in enumerate(fichas, 1):
            self.add_item(SelecionarPersonagemButton(idx, nome, user_id))

class SelecionarPersonagemButton(discord.ui.Button):
    def __init__(self, idx, nome, user_id):
        super().__init__(label=f"{idx}. {nome}", style=discord.ButtonStyle.secondary)
        self.idx = idx
        self.nome = nome
        self.user_id = user_id
        self.tooltip = f"Selecionar personagem {nome} para visualizar o mapa. [Acessível]"
        self.emoji = "ℹ️"
    async def callback(self, interaction: discord.Interaction):
        from database import get_personagem_por_usuario
        personagem = get_personagem_por_usuario(str(self.user_id))
        pid, nome, pos = personagem
        x, y = map(int, pos.split(","))
        evento = MAPA_EVENTOS.get((x, y))
        embed = gerar_embed_mapa(nome, x, y, evento)
        file = discord.File("data/mapa_rpgium.png", filename="mapa_rpgium.png")
        await interaction.response.send_message(embed=embed, view=MapaView(pid, pos), file=file, ephemeral=True)

class PainelView(PainelJogadorView):
    def __init__(self):
        # Painel principal para on_guild_join
        super().__init__(user_id=None)

print("Bot iniciado! Aguardando conexão com o Discord...")

bot.run(TOKEN)
