from fastapi import FastAPI, HTTPException, Body, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any
import database
import os
import requests

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

# Exemplo de dados em memória (substituir por banco real)
skill_trees: Dict[int, List[Dict[str, Any]]] = {}
achievements: Dict[int, List[Dict[str, Any]]] = {}
crafting: Dict[int, List[Dict[str, Any]]] = {}
economy: Dict[int, Dict[str, Any]] = {}
guilds: Dict[int, Dict[str, Any]] = {}
# --- Mercado de Jogadores (Marketplace) ---
marketplace: List[Dict[str, Any]] = []

@app.get("/characters/{user_id}/skilltree", response_model=List[Dict[str, Any]])
def get_skilltree(user_id: int):
    """Retorna a árvore de habilidades do personagem."""
    return skill_trees.get(user_id, [
        {"id": "root", "name": "Aptidão Básica", "description": "Base para todas as habilidades.", "unlocked": True, "icon": "🌱", "children": [
            {"id": "atk1", "name": "Ataque Rápido", "description": "Desbloqueia ataque rápido.", "unlocked": False, "icon": "⚡"},
            {"id": "def1", "name": "Defesa Básica", "description": "Desbloqueia defesa básica.", "unlocked": False, "icon": "🛡️", "children": [
                {"id": "def2", "name": "Barreira Avançada", "description": "Desbloqueia barreira avançada.", "unlocked": False, "icon": "🔰"}
            ]}
        ]}
    ])

@app.post("/characters/{user_id}/skilltree/unlock")
def unlock_skill(user_id: int, skill_id: str):
    """Desbloqueia uma habilidade na árvore do personagem."""
    def unlock(nodes):
        for n in nodes:
            if n["id"] == skill_id:
                n["unlocked"] = True
                return True
            if n.get("children") and unlock(n["children"]):
                return True
        return False
    tree = skill_trees.setdefault(user_id, get_skilltree(user_id))
    if unlock(tree):
        return {"success": True, "message": f"Habilidade {skill_id} desbloqueada."}
    raise HTTPException(status_code=404, detail="Skill não encontrada")

@app.get("/characters/{user_id}/achievements", response_model=List[Dict[str, Any]])
def get_achievements(user_id: int):
    """Retorna as conquistas do personagem."""
    return achievements.get(user_id, [])

@app.post("/characters/{user_id}/achievements/unlock")
def unlock_achievement(user_id: int, nome: str, descricao: str = "", icon: str = "🎖️"):
    """Desbloqueia uma conquista para o personagem."""
    ach = {"nome": nome, "descricao": descricao or f"Conquista especial: {nome}", "icon": icon}
    user_achs = achievements.setdefault(user_id, [])
    user_achs.append(ach)
    return {"success": True, "message": f"Conquista {nome} desbloqueada."}

@app.get("/characters/{user_id}/crafting", response_model=List[Dict[str, Any]])
def get_crafting(user_id: int):
    """Retorna os itens craftados/upgrades do personagem."""
    return crafting.get(user_id, [])

@app.post("/characters/{user_id}/crafting")
def craft_item(user_id: int, nome: str, materiais: List[str], upgrade: bool = False):
    """Cria ou faz upgrade de um item para o personagem."""
    item = {"nome": nome, "materiais": materiais, "upgrade": upgrade}
    user_craft = crafting.setdefault(user_id, [])
    user_craft.append(item)
    return {"success": True, "message": f"Item {nome} {'upgradado' if upgrade else 'craftado'} com sucesso."}

@app.get("/characters/{user_id}/economy", response_model=Dict[str, Any])
def get_economy(user_id: int):
    """Retorna dados econômicos do personagem: moedas, banco, histórico, etc."""
    return economy.get(user_id, {"moedas": 100, "banco": 0, "historico": []})

@app.post("/characters/{user_id}/economy/transfer")
def transfer(user_id: int, destino_id: int, valor: int):
    """Transfere moedas entre personagens."""
    eco = economy.setdefault(user_id, {"moedas": 100, "banco": 0, "historico": []})
    if eco["moedas"] < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    eco["moedas"] -= valor
    eco["historico"].append({"tipo": "envio", "destino": destino_id, "valor": valor})
    dest = economy.setdefault(destino_id, {"moedas": 100, "banco": 0, "historico": []})
    dest["moedas"] += valor
    dest["historico"].append({"tipo": "recebimento", "origem": user_id, "valor": valor})
    return {"success": True, "message": f"Transferência de {valor} moedas realizada."}

@app.post("/characters/{user_id}/economy/bank")
def bank_action(user_id: int, valor: int, acao: str):
    """Deposita ou saca moedas do banco virtual."""
    eco = economy.setdefault(user_id, {"moedas": 100, "banco": 0, "historico": []})
    if acao == "depositar":
        if eco["moedas"] < valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        eco["moedas"] -= valor
        eco["banco"] += valor
        eco["historico"].append({"tipo": "deposito", "valor": valor})
    elif acao == "sacar":
        if eco["banco"] < valor:
            raise HTTPException(status_code=400, detail="Saldo bancário insuficiente")
        eco["banco"] -= valor
        eco["moedas"] += valor
        eco["historico"].append({"tipo": "saque", "valor": valor})
    else:
        raise HTTPException(status_code=400, detail="Ação inválida")
    return {"success": True, "message": f"Ação '{acao}' de {valor} moedas realizada."}

def get_guild(guild_id: int):
    return guilds.get(guild_id, {"nome": "", "membros": [], "ranking": 0, "conquistas": [], "guerras": []})

@app.get("/guilds", response_model=List[Dict[str, Any]])
def list_guilds():
    """Lista todas as guildas/clãs."""
    return list(guilds.values())

@app.post("/guilds/create")
def create_guild(nome: str, fundador_id: int):
    """Cria uma nova guilda/clã."""
    guild_id = len(guilds) + 1
    guild = {"id": guild_id, "nome": nome, "membros": [fundador_id], "ranking": 0, "conquistas": [], "guerras": []}
    guilds[guild_id] = guild
    return {"success": True, "guild": guild}

@app.post("/guilds/{guild_id}/join")
def join_guild(guild_id: int, user_id: int):
    """Adiciona um membro à guilda."""
    guild = guilds.get(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guilda não encontrada")
    if user_id not in guild["membros"]:
        guild["membros"].append(user_id)
    return {"success": True, "guild": guild}

@app.get("/guilds/ranking", response_model=List[Dict[str, Any]])
def guild_ranking():
    """Ranking global/local de guildas."""
    return sorted(guilds.values(), key=lambda g: g["ranking"], reverse=True)

@app.post("/guilds/{guild_id}/war")
def guild_war(guild_id: int, target_id: int):
    """Inicia uma guerra entre guildas."""
    guild = guilds.get(guild_id)
    target = guilds.get(target_id)
    if not guild or not target:
        raise HTTPException(status_code=404, detail="Guilda não encontrada")
    guild["guerras"].append(target_id)
    target["guerras"].append(guild_id)
    return {"success": True, "message": f"Guerra iniciada entre {guild['nome']} e {target['nome']}!"}

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
