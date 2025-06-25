// Tipos relacionados a autenticação e usuários
export interface User {
  id: string;
  username: string;
  avatar: string;
  discordId: string;
  isAdmin: boolean;
  servers: string[];
  economy: Economy;
  characters: Character[];
}

export interface Economy {
  coins: number;
  bank: number;
  history: Transaction[];
}

export interface Transaction {
  id: string;
  type: 'deposit' | 'withdraw' | 'transfer' | 'purchase' | 'sale';
  amount: number;
  description: string;
  date: string;
  relatedUserId?: string;
}

// Tipos relacionados a personagens e fichas
export interface Character {
  id: string;
  userId: string;
  name: string;
  race: string;
  class: string;
  level: number;
  xp: number;
  status: 'active' | 'inactive' | 'dead';
  attributes: CharacterAttributes;
  inventory: Inventory;
  skills: Skill[];
  position: MapPosition;
  avatarUrl?: string;
  campaignId?: string;
}

export interface CharacterAttributes {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
  hp: number;
  maxHp: number;
  mana: number;
  maxMana: number;
}

// Tipos relacionados a inventário e itens
export interface Inventory {
  id: string;
  characterId: string;
  items: Item[];
  maxWeight: number;
  currentWeight: number;
}

export interface Item {
  id: string;
  name: string;
  description: string;
  type: 'weapon' | 'armor' | 'consumable' | 'material' | 'quest';
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
  weight: number;
  quantity: number;
  value: number;
  effects?: ItemEffect[];
}

export interface ItemEffect {
  type: 'buff' | 'debuff' | 'damage' | 'heal';
  attribute: string;
  value: number;
  duration?: number;
}

// Tipos relacionados a habilidades
export interface Skill {
  id: string;
  name: string;
  description: string;
  level: number;
  maxLevel: number;
  effects: SkillEffect[];
  requirements: SkillRequirement[];
  unlocked: boolean;
  icon?: string;
}

export interface SkillEffect {
  type: 'damage' | 'heal' | 'buff' | 'debuff';
  value: number;
  duration?: number;
  target: 'self' | 'single' | 'area';
}

export interface SkillRequirement {
  type: 'level' | 'skill' | 'attribute';
  value: number;
  skillId?: string;
}

// Tipos relacionados a campanhas
export interface Campaign {
  id: string;
  name: string;
  description: string;
  masterId: string;
  players: CampaignPlayer[];
  status: 'active' | 'paused' | 'finished';
  created: string;
  lastSession?: string;
  nextSession?: string;
}

export interface CampaignPlayer {
  userId: string;
  characterId: string;
  joinedAt: string;
  status: 'active' | 'inactive';
}

// Tipos relacionados ao mapa
export interface MapPosition {
  x: number;
  y: number;
  region: string;
  discovered: boolean;
}

export interface MapEvent {
  id: string;
  type: 'combat' | 'dialog' | 'treasure' | 'quest';
  title: string;
  description: string;
  requirements?: EventRequirement[];
  rewards?: Reward[];
}

export interface EventRequirement {
  type: 'level' | 'item' | 'quest' | 'skill';
  value: string | number;
}

export interface Reward {
  type: 'xp' | 'item' | 'gold' | 'skill';
  value: number | string;
  quantity?: number;
}

// Tipos relacionados a missões e conquistas
export interface Quest {
  id: string;
  title: string;
  description: string;
  type: 'main' | 'side' | 'daily' | 'weekly';
  objectives: QuestObjective[];
  rewards: Reward[];
  status: 'available' | 'active' | 'completed' | 'failed';
  deadline?: string;
}

export interface QuestObjective {
  id: string;
  description: string;
  progress: number;
  target: number;
  completed: boolean;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  progress: number;
  completed: boolean;
  completedAt?: string;
  rewards?: Reward[];
}

// Tipos relacionados ao marketplace
export interface MarketItem {
  id: string;
  sellerId: string;
  name: string;
  description: string;
  type: string;
  price: number;
  quantity: number;
  sold: boolean;
  buyerId?: string;
  listedAt: string;
  soldAt?: string;
}

// Tipos relacionados a guildas/clãs
export interface Guild {
  id: string;
  name: string;
  description: string;
  founderId: string;
  members: GuildMember[];
  level: number;
  xp: number;
  ranking: number;
  achievements: Achievement[];
  wars: GuildWar[];
}

export interface GuildMember {
  userId: string;
  role: 'leader' | 'officer' | 'member';
  joinedAt: string;
  contributions: number;
}

export interface GuildWar {
  id: string;
  targetGuildId: string;
  status: 'declared' | 'active' | 'finished';
  startDate: string;
  endDate?: string;
  winner?: string;
}

// Tipos relacionados a temas e personalização
export interface Theme {
  primaryBg: string;
  secondaryBg: string;
  accent: string;
  text: string;
  card: string;
  cardBorder: string;
  icon: string;
  label: string;
}

export interface Customization {
  theme: string;
  avatar?: string;
  bannerUrl?: string;
  preferences: {
    notifications: boolean;
    sound: boolean;
    language: string;
  };
}

// Tipos relacionados a integração com IA
export interface AIConfig {
  model: string;
  temperature: number;
  maxTokens: number;
  presence_penalty: number;
  frequency_penalty: number;
}

export interface AIResponse {
  text: string;
  tokens: number;
  finish_reason: string;
}

export interface NPCData {
  id: string;
  name: string;
  role: string;
  personality: string;
  knowledge: string[];
  responses: AIResponse[];
}

// Tipos de eventos e logs
export interface GameEvent {
  id: string;
  type: string;
  data: any;
  timestamp: string;
  userId?: string;
  characterId?: string;
}

export interface CombatLog {
  id: string;
  type: 'attack' | 'defense' | 'skill' | 'item' | 'effect';
  source: {
    id: string;
    name: string;
    type: 'player' | 'npc' | 'environment';
  };
  target?: {
    id: string;
    name: string;
    type: 'player' | 'npc' | 'environment';
  };
  value: number;
  timestamp: string;
  details?: any;
}
