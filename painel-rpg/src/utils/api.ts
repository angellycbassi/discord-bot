import axios from "axios";

const api = axios.create({
  baseURL:
    typeof window !== "undefined"
      ? process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      : "",
  withCredentials: true,
});

export default api;

export async function fetchUser(sessionId?: string) {
  // Busca usuário autenticado pelo session_id
  const { data } = await api.get("/usuarios/me", {
    params: { session_id: sessionId || getSessionId() },
  });
  return data;
}

export async function fetchCharacters(discordId?: string) {
  // Busca personagens do usuário logado
  const { data } = await api.get(`/personagens/${discordId || getUserId()}`);
  return data;
}

export async function createCharacter(payload: any) {
  const { data } = await api.post("/personagens/criar", payload);
  return data;
}

export async function updateCharacter(id: string, payload: any) {
  // Não implementado no backend, mas pode ser adicionado
  // const { data } = await api.put(`/personagens/${id}`, payload);
  // return data;
  throw new Error("updateCharacter não implementado no backend");
}

export async function deleteCharacter(id: string) {
  const { data } = await api.delete(`/personagens/${id}`);
  return data;
}

export async function getSkillTree(characterId: string) {
  // Mantém endpoint existente
  const { data } = await api.get(`/characters/${characterId}/skilltree`);
  return data;
}

export async function unlockSkill(characterId: string, skillId: string) {
  const { data } = await api.post(
    `/characters/${characterId}/skilltree/unlock`,
    { skill_id: skillId }
  );
  return data;
}

export async function fetchInventory(personagemId: number) {
  const { data } = await api.get(`/inventario/${personagemId}`);
  return data;
}

export async function fetchCampaigns(discordId?: string) {
  const { data } = await api.get(`/campanhas/${discordId || getUserId()}`);
  return data;
}

// Funções utilitárias para session_id e user_id
function getSessionId() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("session_id") || undefined;
  }
  return undefined;
}
function getUserId() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("discord_id") || undefined;
  }
  return undefined;
}
