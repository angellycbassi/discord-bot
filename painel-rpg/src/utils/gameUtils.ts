// Cálculos de XP e nível
export function calculateLevel(xp: number): number {
  // Fórmula básica: cada nível requer XP = base * (nível atual)^2
  const base = 100;
  return Math.floor(Math.sqrt(xp / base)) + 1;
}

export function calculateXPForNextLevel(currentLevel: number): number {
  const base = 100;
  return base * Math.pow(currentLevel, 2);
}

export function calculateXPProgress(xp: number): number {
  const currentLevel = calculateLevel(xp);
  const currentLevelXP = calculateXPForNextLevel(currentLevel - 1);
  const nextLevelXP = calculateXPForNextLevel(currentLevel);
  return ((xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100;
}

// Formato de moedas e números
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('pt-BR').format(amount);
}

export function formatNumber(number: number): string {
  if (number >= 1000000) {
    return `${(number / 1000000).toFixed(1)}M`;
  }
  if (number >= 1000) {
    return `${(number / 1000).toFixed(1)}K`;
  }
  return number.toString();
}

// Formatação de data/hora
export function formatDate(date: Date | string): string {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(new Date(date));
}

export function formatDateTime(date: Date | string): string {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date));
}

export function formatTimeAgo(date: Date | string): string {
  const now = new Date();
  const past = new Date(date);
  const diff = Math.floor((now.getTime() - past.getTime()) / 1000);

  const intervals = {
    ano: 31536000,
    mês: 2592000,
    semana: 604800,
    dia: 86400,
    hora: 3600,
    minuto: 60,
    segundo: 1,
  };

  for (const [unit, seconds] of Object.entries(intervals)) {
    const interval = Math.floor(diff / seconds);
    if (interval >= 1) {
      return `há ${interval} ${unit}${interval !== 1 ? 's' : ''}`;
    }
  }

  return 'agora mesmo';
}

// Rolagem de dados
export function rollDice(diceString: string): { total: number; rolls: number[] } {
  const [count, sides] = diceString.toLowerCase().split('d').map(Number);
  const rolls: number[] = [];
  let total = 0;

  for (let i = 0; i < count; i++) {
    const roll = Math.floor(Math.random() * sides) + 1;
    rolls.push(roll);
    total += roll;
  }

  return { total, rolls };
}

export function rollWithAdvantage(): { total: number; rolls: [number, number] } {
  const roll1 = Math.floor(Math.random() * 20) + 1;
  const roll2 = Math.floor(Math.random() * 20) + 1;
  return { total: Math.max(roll1, roll2), rolls: [roll1, roll2] };
}

export function rollWithDisadvantage(): { total: number; rolls: [number, number] } {
  const roll1 = Math.floor(Math.random() * 20) + 1;
  const roll2 = Math.floor(Math.random() * 20) + 1;
  return { total: Math.min(roll1, roll2), rolls: [roll1, roll2] };
}

// Formatação de texto para chat/descrições
export function parseEmojis(text: string): string {
  const emojiMap: Record<string, string> = {
    ':sword:': '⚔️',
    ':shield:': '🛡️',
    ':magic:': '✨',
    ':potion:': '🧪',
    ':gold:': '💰',
    ':heart:': '❤️',
    ':skull:': '💀',
    ':dragon:': '🐉',
    ':scroll:': '📜',
    ':gem:': '💎',
    ':fire:': '🔥',
    ':ice:': '❄️',
    ':lightning:': '⚡',
  };

  return text.replace(/:\w+:/g, match => emojiMap[match] || match);
}

export function formatChatMessage(message: string): string {
  return parseEmojis(message)
    .replace(/\*\*(.*?)\*\*/g, '\x1b[1m$1\x1b[0m') // Negrito
    .replace(/\*(.*?)\*/g, '\x1b[3m$1\x1b[0m'); // Itálico
}

// Validação de dados
export function validateCharacterName(name: string): boolean {
  return name.length >= 3 && name.length <= 32 && /^[a-zA-Z\s'-]+$/.test(name);
}

export function validateDiscordId(id: string): boolean {
  return /^\d{17,19}$/.test(id);
}

// Geradores de conteúdo aleatório
export const generateRandomLoot = (rarity: string = 'common'): string[] => {
  const lootTables = {
    common: ['Poção de Cura Menor', 'Pergaminho Básico', 'Adaga Simples', 'Ervas Comuns'],
    uncommon: ['Poção de Mana', 'Armadura de Couro', 'Amuleto Mágico', 'Gemas Brutas'],
    rare: ['Espada Encantada', 'Grimório Místico', 'Elixir de Força', 'Cristais Mágicos'],
    epic: ['Arma Lendária', 'Armadura de Dragão', 'Varinha Ancestral', 'Relíquia Sagrada'],
    legendary: ['Artefato Divino', 'Arma do Herói', 'Amuleto dos Deuses', 'Orbe do Poder'],
  };

  return lootTables[rarity as keyof typeof lootTables] || lootTables.common;
};
