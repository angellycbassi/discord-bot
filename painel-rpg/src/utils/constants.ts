export const THEMES = {
  dark: {
    primaryBg: '#18181b',
    secondaryBg: '#23232b',
    accent: '#ffd700',
    text: '#f4f4f5',
    card: '#23232b',
    cardBorder: '#333',
    icon: '🌑',
    label: 'Dark Mode'
  },
  light: {
    primaryBg: '#f4f4f5',
    secondaryBg: '#fff',
    accent: '#23232b',
    text: '#23232b',
    card: '#fff',
    cardBorder: '#ddd',
    icon: '☀️',
    label: 'Light Mode'
  },
  medieval: {
    primaryBg: '#2d1e13',
    secondaryBg: '#3b2716',
    accent: '#bfa76a',
    text: '#f5e6c8',
    card: '#3b2716',
    cardBorder: '#bfa76a',
    icon: '🛡️',
    label: 'Medieval'
  },
  cyberpunk: {
    primaryBg: '#0f0026',
    secondaryBg: '#1a0033',
    accent: '#ff00cc',
    text: '#00fff7',
    card: '#1a0033',
    cardBorder: '#ff00cc',
    icon: '🤖',
    label: 'Cyberpunk'
  },
  forest: {
    primaryBg: '#1b2e1b',
    secondaryBg: '#284d28',
    accent: '#7ed957',
    text: '#eaffea',
    card: '#284d28',
    cardBorder: '#7ed957',
    icon: '🌲',
    label: 'Forest'
  }
};

export type ThemeName = keyof typeof THEMES;

export const CHARACTER_CLASSES = [
  { id: 'warrior', name: 'Guerreiro', icon: '⚔️' },
  { id: 'mage', name: 'Mago', icon: '🔮' },
  { id: 'rogue', name: 'Ladino', icon: '🗡️' },
  { id: 'priest', name: 'Sacerdote', icon: '✨' },
  { id: 'ranger', name: 'Caçador', icon: '🏹' },
  { id: 'paladin', name: 'Paladino', icon: '🛡️' },
  { id: 'druid', name: 'Druida', icon: '🍃' },
  { id: 'bard', name: 'Bardo', icon: '🎵' },
  { id: 'warlock', name: 'Bruxo', icon: '👻' },
];

export const CHARACTER_RACES = [
  { id: 'human', name: 'Humano', icon: '👤' },
  { id: 'elf', name: 'Elfo', icon: '🧝' },
  { id: 'dwarf', name: 'Anão', icon: '⛏️' },
  { id: 'orc', name: 'Orc', icon: '👹' },
  { id: 'halfling', name: 'Halfling', icon: '🦶' },
  { id: 'dragonborn', name: 'Draconato', icon: '🐲' },
  { id: 'tiefling', name: 'Tiefling', icon: '😈' },
  { id: 'gnome', name: 'Gnomo', icon: '🎩' },
];

export const ITEM_RARITIES = [
  { id: 'common', name: 'Comum', color: '#9d9d9d' },
  { id: 'uncommon', name: 'Incomum', color: '#1eff00' },
  { id: 'rare', name: 'Raro', color: '#0070dd' },
  { id: 'epic', name: 'Épico', color: '#a335ee' },
  { id: 'legendary', name: 'Lendário', color: '#ff8000' },
];

export const ITEM_CATEGORIES = [
  { id: 'weapon', name: 'Arma', icon: '⚔️' },
  { id: 'armor', name: 'Armadura', icon: '🛡️' },
  { id: 'potion', name: 'Poção', icon: '🧪' },
  { id: 'scroll', name: 'Pergaminho', icon: '📜' },
  { id: 'material', name: 'Material', icon: '💎' },
  { id: 'consumable', name: 'Consumível', icon: '🍖' },
  { id: 'quest', name: 'Item de Missão', icon: '❗' },
  { id: 'key', name: 'Chave', icon: '🔑' },
];

export const AI_MODELS = [
  { key: 'stable-diffusion', name: 'Stable Diffusion' },
  { key: 'dalle', name: 'DALL-E' },
  { key: 'midjourney', name: 'Midjourney' },
];

export const AVATAR_PRESETS = [
  'guerreiro medieval, armadura dourada, fundo de floresta',
  'feiticeira cyberpunk, cabelos azuis, fundo neon',
  'anão da floresta, machado, fundo verde',
  'elfo arqueiro, capa esvoaçante, fundo de montanhas',
  'mago ancião, túnica roxa, fundo de biblioteca',
];

export const MAP_EVENTS = {
  'default': 'Você está em uma área tranquila.',
  'forest': 'Uma densa floresta se estende à sua frente.',
  'mountain': 'Montanhas imponentes se erguem no horizonte.',
  'dungeon': 'A entrada de uma masmorra sombria.',
  'village': 'Uma pequena vila acolhedora.',
  'castle': 'Um castelo majestoso domina a paisagem.',
  'cave': 'Uma caverna misteriosa se abre na rocha.',
  'ruins': 'Ruínas antigas contam histórias esquecidas.',
  'portal': 'Um portal mágico pulsa com energia arcana.',
};

export const BREAKPOINTS = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};
