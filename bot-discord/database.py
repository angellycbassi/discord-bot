"""
Módulo de acesso ao banco de dados SQLite para o bot de RPG.
Gerencia a criação de tabelas e operações CRUD para fichas de personagem.
"""
import sqlite3
from contextlib import closing

DB_PATH = 'data/rpgbot.db'

# Criação automática do banco e tabela, se não existir
def init_db():
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    # Tabela de usuários (pode ser expandida para preferências, idioma, etc)
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id TEXT UNIQUE NOT NULL,
        nome TEXT,
        ouro INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        conquistas TEXT DEFAULT '',
        posicao_mapa TEXT DEFAULT '0,0',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    # Tabela de personagens
    c.execute('''CREATE TABLE IF NOT EXISTS personagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        nome TEXT,
        raca TEXT,
        classe TEXT,
        xp INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        status TEXT DEFAULT 'ativo',
        campanha_id INTEGER,
        posicao_mapa TEXT DEFAULT '0,0',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')
    # Tabela de inventário
    c.execute('''CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personagem_id INTEGER,
        item TEXT,
        categoria TEXT,
        peso REAL DEFAULT 0,
        descricao TEXT,
        quantidade INTEGER DEFAULT 1,
        data_adicionado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(personagem_id) REFERENCES personagens(id)
    )''')
    # Tabela de campanhas
    c.execute('''CREATE TABLE IF NOT EXISTS campanhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        mestre_id TEXT,
        descricao TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    # Tabela de missões
    c.execute('''CREATE TABLE IF NOT EXISTS missoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        recompensa TEXT,
        progresso TEXT,
        personagem_id INTEGER,
        campanha_id INTEGER,
        status TEXT DEFAULT 'ativa',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(personagem_id) REFERENCES personagens(id),
        FOREIGN KEY(campanha_id) REFERENCES campanhas(id)
    )''')
    # Tabela de economia/histórico
    c.execute('''CREATE TABLE IF NOT EXISTS economia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tipo TEXT,
        valor INTEGER,
        descricao TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')
    # Tabela de eventos/conquistas
    c.execute('''CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personagem_id INTEGER,
        tipo TEXT,
        descricao TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(personagem_id) REFERENCES personagens(id)
    )''')
    # Tabela de mapa (pode ser expandida para mapas customizados)
    c.execute('''CREATE TABLE IF NOT EXISTS mapa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        posicao TEXT,
        desbloqueado_por TEXT,
        tipo TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS avatar_personagem (
        ficha_id INTEGER PRIMARY KEY,
        url TEXT
    )''')
    # --- Marketplace (mercado de jogadores/itens) ---
    c.execute('''CREATE TABLE IF NOT EXISTS marketplace (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendedor_id INTEGER,
        item_nome TEXT,
        preco INTEGER,
        descricao TEXT,
        tipo TEXT,
        vendido INTEGER DEFAULT 0,
        comprador_id INTEGER
    )''')
    # Tabela de histórico de avatares
    c.execute('''CREATE TABLE IF NOT EXISTS avatar_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personagem_id INTEGER,
        url TEXT,
        tipo TEXT,
        prompt TEXT,
        modelo TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# Funções utilitárias para integração cruzada

def criar_usuario(discord_id, nome):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO usuarios (discord_id, nome) VALUES (?, ?)', (discord_id, nome))
    conn.commit()
    conn.close()

def criar_personagem(discord_id, nome, raca, classe, campanha_id=None):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('SELECT id FROM usuarios WHERE discord_id = ?', (discord_id,))
    usuario = c.fetchone()
    if not usuario:
        criar_usuario(discord_id, nome)
        c.execute('SELECT id FROM usuarios WHERE discord_id = ?', (discord_id,))
        usuario = c.fetchone()
    usuario_id = usuario[0]
    c.execute('INSERT INTO personagens (usuario_id, nome, raca, classe, campanha_id) VALUES (?, ?, ?, ?, ?)',
              (usuario_id, nome, raca, classe, campanha_id))
    conn.commit()
    conn.close()

def listar_personagens(discord_id):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('SELECT id FROM usuarios WHERE discord_id = ?', (discord_id,))
    usuario = c.fetchone()
    if not usuario:
        return []
    usuario_id = usuario[0]
    c.execute('SELECT nome, raca, classe, xp, nivel, status FROM personagens WHERE usuario_id = ?', (usuario_id,))
    fichas = c.fetchall()
    conn.close()
    return fichas

def listar_inventario(personagem_id):
    """Retorna todos os itens do inventário de um personagem."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT item, categoria, quantidade, descricao FROM inventario WHERE personagem_id = ?', (personagem_id,))
    itens = c.fetchall()
    conn.close()
    return itens


def listar_campanhas(discord_id):
    """Retorna todas as campanhas em que o usuário possui personagens."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM usuarios WHERE discord_id = ?', (discord_id,))
    usuario = c.fetchone()
    if not usuario:
        return []
    usuario_id = usuario[0]
    c.execute('''SELECT DISTINCT campanhas.id, campanhas.nome, campanhas.descricao FROM campanhas 
                 JOIN personagens ON campanhas.id = personagens.campanha_id 
                 WHERE personagens.usuario_id = ? AND campanhas.id IS NOT NULL''', (usuario_id,))
    campanhas = c.fetchall()
    conn.close()
    return campanhas

# Exemplo: ao ganhar XP, atualizar personagem e usuário

def adicionar_xp(discord_id, personagem_id, xp):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    # Atualiza XP do personagem
    c.execute('UPDATE personagens SET xp = xp + ? WHERE id = ?', (xp, personagem_id))
    # Atualiza XP do usuário
    c.execute('SELECT usuario_id FROM personagens WHERE id = ?', (personagem_id,))
    usuario_id = c.fetchone()[0]
    c.execute('UPDATE usuarios SET xp = xp + ? WHERE id = ?', (xp, usuario_id))
    conn.commit()
    conn.close()

# Exemplo: ao adicionar item, atualizar inventário e painel

def adicionar_item(personagem_id, item, categoria, peso, descricao, quantidade=1):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('''INSERT INTO inventario (personagem_id, item, categoria, peso, descricao, quantidade)
                 VALUES (?, ?, ?, ?, ?, ?)''', (personagem_id, item, categoria, peso, descricao, quantidade))
    conn.commit()
    conn.close()

# Exemplo: ao remover personagem, remover inventário, missões, eventos, etc

def remover_personagem(personagem_id):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('DELETE FROM inventario WHERE personagem_id = ?', (personagem_id,))
    c.execute('DELETE FROM missoes WHERE personagem_id = ?', (personagem_id,))
    c.execute('DELETE FROM eventos WHERE personagem_id = ?', (personagem_id,))
    c.execute('DELETE FROM personagens WHERE id = ?', (personagem_id,))
    conn.commit()
    conn.close()

def get_personagem_por_usuario(discord_id):
    """Retorna o primeiro personagem do usuário (para simplificação do painel)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, nome, posicao_mapa FROM personagens WHERE usuario_id = (SELECT id FROM usuarios WHERE discord_id = ?) LIMIT 1', (discord_id,))
    personagem = c.fetchone()
    conn.close()
    return personagem


def atualizar_posicao_personagem(personagem_id, nova_posicao):
    """Atualiza a posição do personagem no mapa."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE personagens SET posicao_mapa = ? WHERE id = ?', (nova_posicao, personagem_id))
    conn.commit()
    conn.close()

# Salva o link do avatar customizado para uma ficha
def set_avatar_personagem(ficha_id, url):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('''INSERT INTO avatar_personagem (ficha_id, url) VALUES (?, ?)
        ON CONFLICT(ficha_id) DO UPDATE SET url=excluded.url''', (ficha_id, url))
    conn.commit()
    conn.close()

# Recupera o link do avatar customizado de uma ficha
def get_avatar_personagem(ficha_id):
    conn = sqlite3.connect('data/rpgbot.db')
    c = conn.cursor()
    c.execute('''SELECT url FROM avatar_personagem WHERE ficha_id = ?''', (ficha_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# --- Marketplace (mercado de jogadores/itens) ---
def criar_tabela_marketplace():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS marketplace (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendedor_id INTEGER,
        item_nome TEXT,
        preco INTEGER,
        descricao TEXT,
        tipo TEXT,
        vendido INTEGER DEFAULT 0,
        comprador_id INTEGER
    )''')
    conn.commit()
    conn.close()

def adicionar_item_marketplace(vendedor_id, item_nome, preco, descricao, tipo="item"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO marketplace (vendedor_id, item_nome, preco, descricao, tipo, vendido) VALUES (?, ?, ?, ?, ?, 0)''',
              (vendedor_id, item_nome, preco, descricao, tipo))
    conn.commit()
    item_id = c.lastrowid
    conn.close()
    return item_id

def listar_marketplace():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, vendedor_id, item_nome, preco, descricao, tipo, vendido, comprador_id FROM marketplace')
    itens = c.fetchall()
    conn.close()
    return [
        {"id": row[0], "vendedor_id": row[1], "item_nome": row[2], "preco": row[3], "descricao": row[4], "tipo": row[5], "vendido": bool(row[6]), "comprador_id": row[7]} for row in itens
    ]

def comprar_item_marketplace(item_id, comprador_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT vendedor_id, preco, vendido FROM marketplace WHERE id = ?', (item_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False, "Item não encontrado."
    vendedor_id, preco, vendido = row
    if vendido:
        conn.close()
        return False, "Item já vendido."
    # Aqui você pode adicionar lógica de débito/crédito de moedas
    c.execute('UPDATE marketplace SET vendido = 1, comprador_id = ? WHERE id = ?', (comprador_id, item_id))
    conn.commit()
    conn.close()
    return True, "Compra realizada com sucesso."

def adicionar_avatar_history(personagem_id, url, tipo, prompt=None, modelo=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO avatar_history (personagem_id, url, tipo, prompt, modelo) VALUES (?, ?, ?, ?, ?)''',
              (personagem_id, url, tipo, prompt, modelo))
    conn.commit()
    conn.close()

def listar_avatar_history(personagem_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT url, tipo, prompt, modelo, data FROM avatar_history WHERE personagem_id = ? ORDER BY data DESC''', (personagem_id,))
    rows = c.fetchall()
    conn.close()
    return [
        {"url": row[0], "tipo": row[1], "prompt": row[2], "modelo": row[3], "data": row[4]} for row in rows
    ]

def criar_tabela_avatar_history():
    """Cria a tabela de histórico de avatares se não existir (implementação inicial)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS avatar_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER,
        url TEXT,
        tipo TEXT,
        prompt TEXT,
        modelo TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
