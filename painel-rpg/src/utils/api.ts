import axios from "axios";

const api = axios.create({
  baseURL:
    typeof window !== "undefined"
      ? process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      : "",
  withCredentials: true,
});

export default api;

export async function fetchUser() {
  const { data } = await api.get("/auth/me");
  return data;
}

export async function fetchCharacters(userId?: string) {
  // Busca personagens do usuário logado
  const { data } = await api.get(`/characters?user_id=${userId || ""}`);
  return data;
}

export async function createCharacter(payload: any) {
  const { data } = await api.post("/characters", payload);
  return data;
}

export async function updateCharacter(id: string, payload: any) {
  const { data } = await api.put(`/characters/${id}`, payload);
  return data;
}

export async function deleteCharacter(id: string) {
  const { data } = await api.delete(`/characters/${id}`);
  return data;
}

export async function getSkillTree(characterId: string) {
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

export async function fetchInventory(characterId: number) {
  const { data } = await api.get(`/characters/${characterId}/inventory`);
  return data;
}

export async function fetchAdventures() {
  const { data } = await api.get("/adventures");
  return data;
}

export async function fetchCampaigns() {
  const { data } = await api.get("/campaigns");
  return data;
}

export async function fetchQuests() {
  const { data } = await api.get("/quests");
  return data;
}

export async function fetchEconomy() {
  const { data } = await api.get("/economy");
  return data;
}

export async function fetchReports() {
  const { data } = await api.get("/reports");
  return data;
}

// Outras funções: fetchCampaigns, etc. podem ser adicionadas conforme as próximas etapas.
