import axios from "axios";

const api = axios.create({
  baseURL:
    typeof window !== "undefined"
      ? process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"
      : "",
  withCredentials: true,
});

export async function fetchUser() {
  const { data } = await api.get("/auth/me");
  return data;
}

export async function fetchCharacters() {
  const { data } = await api.get("/characters");
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
