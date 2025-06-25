from fastapi import FastAPI, HTTPException, Body, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any
import database
import os
import requests
from fastapi import Depends, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.responses import RedirectResponse
import uuid

app = FastAPI(title="RPGium API", description="API REST do bot RPGium para integração com painel web.")

# Permitir CORS para o painel web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir a pasta de avatares como arquivos estáticos
app.mount("/static/avatars", StaticFiles(directory="data/avatars"), name="avatars")

# --- SKILLTREE REAL ---
@app.get("/characters/{personagem_id}/skilltree", response_model=List[Dict[str, Any]])
def get_skilltree(personagem_id: int):
    # Exemplo: skilltree básica fixa, pode ser expandida para salvar/desbloquear no banco
    return [
        {"id": "root", "name": "Aptidão Básica", "description": "Base para todas as habilidades.", "unlocked": True, "icon": "🌱", "children": [
            {"id": "atk1", "name": "Ataque Rápido", "description": "Desbloqueia ataque rápido.", "unlocked": False, "icon": "⚡"},
            {"id": "def1", "name": "Defesa Básica", "description": "Desbloqueia defesa básica.", "unlocked": False, "icon": "🛡️", "children": [
                {"id": "def2", "name": "Barreira Avançada", "description": "Desbloqueia barreira avançada.", "unlocked": False, "icon": "🔰"}
            ]}
        ]}
    ]

@app.post("/characters/{personagem_id}/skilltree/unlock")
def unlock_skill(personagem_id: int, skill_id: str = Body(...)):
    # Exemplo: desbloqueio fictício, pode ser salvo no banco se desejar persistência
    return {"success": True, "message": f"Habilidade {skill_id} desbloqueada."}

# --- CONQUISTAS REAIS ---
@app.get("/characters/{personagem_id}/achievements", response_model=List[Dict[str, Any]])
def get_achievements(personagem_id: int):
    # Exemplo: buscar conquistas do personagem no banco (ajuste conforme modelo)
    conn = database.sqlite3.connect(database.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT conquistas FROM usuarios WHERE id = (SELECT usuario_id FROM personagens WHERE id = ?)', (personagem_id,))
    row = c.fetchone()
    conn.close()
    if not row or not row[0]:
        return []
    return [{"nome": nome, "descricao": "Conquista desbloqueada", "icon": "🎖️"} for nome in row[0].split(",") if nome]

@app.post("/characters/{personagem_id}/achievements/unlock")
def unlock_achievement(personagem_id: int, nome: str = Body(...), descricao: str = Body(""), icon: str = Body("🎖️")):
    # Salva conquista no campo conquistas do usuário
    conn = database.sqlite3.connect(database.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT usuario_id FROM personagens WHERE id = ?', (personagem_id,))
    usuario = c.fetchone()
    if not usuario:
        conn.close()
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    usuario_id = usuario[0]
    c.execute('SELECT conquistas FROM usuarios WHERE id = ?', (usuario_id,))
    conquistas = c.fetchone()[0] or ''
    conquistas_set = set(conquistas.split(",")) if conquistas else set()
    conquistas_set.add(nome)
    conquistas_str = ",".join(conquistas_set)
    c.execute('UPDATE usuarios SET conquistas = ? WHERE id = ?', (conquistas_str, usuario_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Conquista {nome} desbloqueada."}

# --- CRAFTING REAL (simples) ---
@app.get("/characters/{personagem_id}/crafting", response_model=List[Dict[str, Any]])
def get_crafting(personagem_id: int):
    # Exemplo: buscar itens craftados do inventário
    itens = database.listar_inventario(personagem_id)
    return [i for i in itens if i[1] == "craft"]

@app.post("/characters/{personagem_id}/crafting")
def craft_item(personagem_id: int, nome: str = Body(...), materiais: List[str] = Body(...), upgrade: bool = Body(False)):
    # Adiciona item craftado ao inventário
    database.adicionar_item(personagem_id, nome, "craft", 0, f"Crafted: {','.join(materiais)}", 1)
    return {"success": True, "message": f"Item {nome} {'upgradado' if upgrade else 'craftado'} com sucesso."}

# --- ECONOMIA REAL ---
@app.get("/characters/{personagem_id}/economy", response_model=Dict[str, Any])
def get_economy(personagem_id: int):
    conn = database.sqlite3.connect(database.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT xp, nivel FROM personagens WHERE id = ?', (personagem_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return {"moedas": 0, "banco": 0, "historico": []}
    return {"moedas": row[0], "banco": 0, "historico": []}

@app.post("/characters/{personagem_id}/economy/transfer")
def transfer(personagem_id: int, destino_id: int = Body(...), valor: int = Body(...)):
    # Exemplo: transferir XP como moeda
    conn = database.sqlite3.connect(database.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT xp FROM personagens WHERE id = ?', (personagem_id,))
    xp = c.fetchone()[0]
    if xp < valor:
        conn.close()
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    c.execute('UPDATE personagens SET xp = xp - ? WHERE id = ?', (valor, personagem_id))
    c.execute('UPDATE personagens SET xp = xp + ? WHERE id = ?', (valor, destino_id))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Transferência de {valor} moedas realizada."}

@app.post("/characters/{personagem_id}/economy/bank")
def bank_action(personagem_id: int, valor: int = Body(...), acao: str = Body(...)):
    # Exemplo: banco fictício, pode ser expandido
    return {"success": True, "message": f"Ação '{acao}' de {valor} moedas realizada."}

# --- GUILDAS (simples, sem persistência) ---
@app.get("/guilds", response_model=List[Dict[str, Any]])
def list_guilds():
    return []

@app.post("/guilds/create")
def create_guild(nome: str = Body(...), fundador_id: int = Body(...)):
    return {"success": True, "guild": {"id": 1, "nome": nome, "membros": [fundador_id], "ranking": 0, "conquistas": [], "guerras": []}}

@app.post("/guilds/{guild_id}/join")
def join_guild(guild_id: int, user_id: int = Body(...)):
    return {"success": True, "guild": {"id": guild_id, "membros": [user_id]}}

@app.get("/guilds/ranking", response_model=List[Dict[str, Any]])
def guild_ranking():
    return []

@app.post("/guilds/{guild_id}/war")
def guild_war(guild_id: int, target_id: int = Body(...)):
    return {"success": True, "message": f"Guerra iniciada entre {guild_id} e {target_id}!"}

# --- Mercado de Jogadores (Marketplace) ---
@app.on_event("startup")
def startup_event():
    database.criar_tabela_marketplace()
    database.criar_tabela_avatar_history()

@app.get("/marketplace", response_model=List[Dict[str, Any]], tags=["Marketplace"], summary="Lista todos os itens/jogadores à venda no mercado", response_description="Lista de itens disponíveis no mercado.")
def list_marketplace():
    """Lista todos os itens/jogadores à venda no mercado.
    
    Exemplo de resposta:
    [
      {"id": 1, "vendedor_id": 123, "item_nome": "Espada Lendária", "preco": 500, "descricao": "Item raro", "tipo": "item", "vendido": false, "comprador_id": null}
    ]
    """
    return database.listar_marketplace()

@app.post("/marketplace/add", tags=["Marketplace"], summary="Adiciona um item/jogador ao mercado", response_description="Item adicionado com sucesso.")
def add_market_item(
    vendedor_id: int = Body(..., example=123),
    item_nome: str = Body(..., example="Espada Lendária"),
    preco: int = Body(..., example=500),
    descricao: str = Body("", example="Item raro"),
    tipo: str = Body("item", example="item")
):
    """Adiciona um item/jogador ao mercado.
    
    Exemplo de request:
    {
      "vendedor_id": 123,
      "item_nome": "Espada Lendária",
      "preco": 500,
      "descricao": "Item raro",
      "tipo": "item"
    }
    """
    item_id = database.adicionar_item_marketplace(vendedor_id, item_nome, preco, descricao, tipo)
    return {"success": True, "item_id": item_id}

@app.post("/marketplace/buy", tags=["Marketplace"], summary="Compra um item/jogador do mercado", response_description="Compra realizada com sucesso.")
def buy_market_item(
    comprador_id: int = Body(..., example=456),
    item_id: int = Body(..., example=1)
):
    """Compra um item/jogador do mercado.
    
    Exemplo de request:
    {
      "comprador_id": 456,
      "item_id": 1
    }
    """
    sucesso, msg = database.comprar_item_marketplace(item_id, comprador_id)
    if sucesso:
        return {"success": True, "message": msg}
    raise HTTPException(status_code=404, detail=msg)

@app.post("/characters/{character_id}/avatar", tags=["Personagem"], summary="Upload ou define avatar do personagem", response_description="URL do avatar atualizado.")
def set_avatar(character_id: int, file: UploadFile = File(None), url: str = Form(None)):
    """Faz upload de uma imagem ou define uma URL como avatar do personagem."""
    if file:
        ext = os.path.splitext(file.filename)[1]
        avatar_dir = "data/avatars"
        os.makedirs(avatar_dir, exist_ok=True)
        avatar_path = os.path.join(avatar_dir, f"avatar_{character_id}{ext}")
        with open(avatar_path, "wb") as f:
            f.write(file.file.read())
        avatar_url = f"/static/avatars/avatar_{character_id}{ext}"
    elif url:
        avatar_url = url
    else:
        raise HTTPException(status_code=400, detail="Envie um arquivo ou uma URL.")
    database.set_avatar_personagem(character_id, avatar_url)
    database.adicionar_avatar_history(character_id, avatar_url, tipo="upload" if file else "url")
    return {"url": avatar_url}

@app.get("/characters/{character_id}/avatar/history", tags=["Personagem"], summary="Histórico de avatares", response_description="Lista de avatares anteriores.")
def avatar_history(character_id: int):
    return database.listar_avatar_history(character_id)

@app.post("/characters/{character_id}/avatar/ai", tags=["Personagem"], summary="Gera avatar com IA", response_description="URL do avatar gerado.")
def gerar_avatar_ia(character_id: int, prompt: str = Form(...), modelo: str = Form("stable-diffusion")):
    """Gera um avatar de personagem usando IA (exemplo: Replicate Stable Diffusion)."""
    # Exemplo usando Replicate API (substitua pela sua chave e modelo preferido)
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    if not REPLICATE_API_TOKEN:
        raise HTTPException(status_code=500, detail="Chave da API Replicate não configurada.")
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers={
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "version": "a9758cb8b0...",  # Substitua pelo ID do modelo Stable Diffusion
            "input": {"prompt": prompt}
        }
    )
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Erro ao gerar imagem na IA.")
    prediction = response.json()
    # Espera a imagem ficar pronta (polling simplificado)
    import time
    status = prediction["status"]
    get_url = prediction["urls"]["get"]
    while status not in ("succeeded", "failed"):
        time.sleep(2)
        poll = requests.get(get_url, headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"})
        status = poll.json()["status"]
        prediction = poll.json()
    if status != "succeeded":
        raise HTTPException(status_code=500, detail="A IA não conseguiu gerar a imagem.")
    image_url = prediction["output"][0]
    # Baixa e salva a imagem localmente
    img_data = requests.get(image_url).content
    avatar_dir = "data/avatars"
    os.makedirs(avatar_dir, exist_ok=True)
    avatar_path = os.path.join(avatar_dir, f"avatar_{character_id}_ai.png")
    with open(avatar_path, "wb") as f:
        f.write(img_data)
    avatar_url = f"/static/avatars/avatar_{character_id}_ai.png"
    database.set_avatar_personagem(character_id, avatar_url)
    database.adicionar_avatar_history(character_id, avatar_url, tipo="ia", prompt=prompt, modelo=modelo)
    return {"url": avatar_url}

# --- AUTENTICAÇÃO DISCORD OAUTH2 ---
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:8000/auth/callback")
OAUTH_AUTHORIZE_URL = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify%20email"
OAUTH_TOKEN_URL = "https://discord.com/api/oauth2/token"
OAUTH_USER_URL = "https://discord.com/api/users/@me"

# Sessão simples em memória (substitua por JWT/Redis em produção)
sessions = {}

@app.get("/auth/login")
def login():
    """Redireciona para login Discord OAuth2."""
    return RedirectResponse(OAUTH_AUTHORIZE_URL)

@app.get("/auth/callback")
def auth_callback(code: str):
    """Recebe o callback do Discord OAuth2, troca o code por token e cria sessão."""
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": "identify email"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(OAUTH_TOKEN_URL, data=data, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Falha ao autenticar com Discord")
    token = resp.json()["access_token"]
    user_resp = requests.get(OAUTH_USER_URL, headers={"Authorization": f"Bearer {token}"})
    if user_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Falha ao obter usuário Discord")
    user = user_resp.json()
    # Cria usuário no banco se não existir
    database.criar_usuario(user["id"], user["username"])
    # Gera session_id simples
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"discord_id": user["id"], "username": user["username"]}
    # Retorna session_id para frontend (ideal: cookie seguro ou JWT)
    return {"session_id": session_id, "user": user}

# Dependência para autenticação (exemplo simplificado)
def get_current_user(session_id: str = None):
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return sessions[session_id]

# --- ENDPOINTS REAIS ---
@app.get("/usuarios/me")
def get_me(session_id: str):
    """Retorna dados do usuário autenticado."""
    user = get_current_user(session_id)
    return user

@app.get("/usuarios/{discord_id}")
def get_usuario(discord_id: str):
    """Retorna dados do usuário pelo discord_id."""
    # Exemplo: buscar dados do usuário
    conn = database.sqlite3.connect(database.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, discord_id, nome, ouro, xp, nivel, conquistas, posicao_mapa FROM usuarios WHERE discord_id = ?', (discord_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"id": row[0], "discord_id": row[1], "nome": row[2], "ouro": row[3], "xp": row[4], "nivel": row[5], "conquistas": row[6], "posicao_mapa": row[7]}

@app.get("/personagens/{discord_id}")
def listar_personagens_usuario(discord_id: str):
    """Lista todos os personagens do usuário."""
    fichas = database.listar_personagens(discord_id)
    return [
        {"nome": f[0], "raca": f[1], "classe": f[2], "xp": f[3], "nivel": f[4], "status": f[5]} for f in fichas
    ]

@app.post("/personagens/criar")
def criar_personagem(discord_id: str = Body(...), nome: str = Body(...), raca: str = Body(...), classe: str = Body(...), campanha_id: int = Body(None)):
    """Cria um novo personagem para o usuário."""
    database.criar_personagem(discord_id, nome, raca, classe, campanha_id)
    return {"success": True}

@app.delete("/personagens/{personagem_id}")
def deletar_personagem(personagem_id: int):
    """Remove personagem e dados relacionados."""
    database.remover_personagem(personagem_id)
    return {"success": True}

@app.get("/inventario/{personagem_id}")
def listar_inventario_personagem(personagem_id: int):
    """Lista o inventário do personagem."""
    itens = database.listar_inventario(personagem_id)
    return [
        {"item": i[0], "categoria": i[1], "quantidade": i[2], "descricao": i[3]} for i in itens
    ]

@app.post("/inventario/adicionar")
def adicionar_item_inventario(personagem_id: int = Body(...), item: str = Body(...), categoria: str = Body(...), peso: float = Body(0), descricao: str = Body(""), quantidade: int = Body(1)):
    """Adiciona item ao inventário do personagem."""
    database.adicionar_item(personagem_id, item, categoria, peso, descricao, quantidade)
    return {"success": True}

@app.get("/campanhas/{discord_id}")
def listar_campanhas_usuario(discord_id: str):
    """Lista campanhas em que o usuário possui personagens."""
    campanhas = database.listar_campanhas(discord_id)
    return [
        {"id": c[0], "nome": c[1], "descricao": c[2]} for c in campanhas
    ]
