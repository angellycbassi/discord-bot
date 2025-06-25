import { useEffect, useState } from "react";
import {
  fetchCharacters,
  createCharacter,
  updateCharacter,
  deleteCharacter,
  getSkillTree,
  unlockSkill,
} from "../utils/api";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import Loader from "../components/Loader";
import CharacterForm from "../components/CharacterForm";
import { motion } from "framer-motion";
import SkillTree, { SkillNode } from "../components/SkillTree";
import { useAuth } from "../context/AuthContext";
import { useApi } from "../hooks/useApi";

export default function Characters() {
  const { user } = useAuth();
  const [showForm, setShowForm] = useState(false);
  const [editChar, setEditChar] = useState<any | null>(null);
  const [skills, setSkills] = useState<SkillNode[]>([]);
  const [selectedCharId, setSelectedCharId] = useState<string | null>(null);

  // Busca personagens do usuário logado
  const {
    data: characters = [],
    loading,
    error,
    refetch,
  } = useApi(() => fetchCharacters(user?.id), [user?.id]);

  // Busca skilltree do personagem selecionado
  useEffect(() => {
    if (selectedCharId) {
      getSkillTree(selectedCharId)
        .then(setSkills)
        .catch(() => setSkills([]));
    }
  }, [selectedCharId]);

  // Criação/edição de personagem
  async function handleSubmit(data: any) {
    if (editChar) {
      await updateCharacter(editChar.id, data);
    } else {
      await createCharacter({ ...data, userId: user?.id });
    }
    setShowForm(false);
    setEditChar(null);
    refetch();
  }

  // Exclusão real
  async function handleDelete(id: string) {
    await deleteCharacter(id);
    refetch();
  }

  // Desbloqueio real de skill
  async function handleUnlockSkill(skillId: string) {
    if (!selectedCharId) return;
    await unlockSkill(selectedCharId, skillId);
    const updated = await getSkillTree(selectedCharId);
    setSkills(updated);
  }

  if (loading) return <Loader text="Carregando personagens..." />;
  if (error) return <div>Erro ao carregar personagens.</div>;

  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Personagens</h1>
        <button
          onClick={() => {
            setEditChar(null);
            setShowForm(true);
          }}
          style={{
            marginBottom: 16,
            background: "var(--accent)",
            color: "#fff",
            border: 0,
            borderRadius: 8,
            padding: 8,
            fontWeight: 600,
          }}
        >
          + Criar Personagem
        </button>
        {showForm && (
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            <CharacterForm onSubmit={handleSubmit} initial={editChar} />
          </motion.div>
        )}
        <ul>
          {characters.map((c: any, i: number) => (
            <motion.li
              key={c.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              layout
              style={{
                marginBottom: 12,
                background: "var(--background-secondary)",
                borderRadius: 8,
                padding: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              }}
            >
              <strong>{c.nome}</strong> - {c.raca} - {c.classe} - XP: {c.xp}
              <button
                onClick={() => {
                  setEditChar(c);
                  setShowForm(true);
                }}
                style={{
                  marginLeft: 16,
                  background: "#444",
                  color: "#fff",
                  border: 0,
                  borderRadius: 6,
                  padding: "2px 8px",
                }}
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(c.id)}
                style={{
                  marginLeft: 8,
                  background: "#c00",
                  color: "#fff",
                  border: 0,
                  borderRadius: 6,
                  padding: "2px 8px",
                }}
              >
                Excluir
              </button>
              <button
                onClick={() => setSelectedCharId(c.id)}
                style={{
                  marginLeft: 8,
                  background: "#0af",
                  color: "#fff",
                  border: 0,
                  borderRadius: 6,
                  padding: "2px 8px",
                }}
              >
                Ver Skills
              </button>
            </motion.li>
          ))}
        </ul>
        {selectedCharId && (
          <section style={{ margin: "32px 0" }}>
            <h2>Árvore de Habilidades</h2>
            <SkillTree tree={skills} onUnlock={handleUnlockSkill} />
          </section>
        )}
      </main>
    </ProtectedRoute>
  );
}
