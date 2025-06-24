import { useEffect, useState } from "react";
import { fetchCharacters } from "../utils/api";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import Loader from "../components/Loader";
import CharacterForm from "../components/CharacterForm";
import { motion } from "framer-motion";
import SkillTree, { SkillNode } from "../components/SkillTree";

// Definição do tipo para personagem
interface Character {
  nome: string;
  raca: string;
  classe: string;
  xp: number;
}

export default function Characters() {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editChar, setEditChar] = useState<Character | null>(null);
  const [skills, setSkills] = useState<SkillNode[]>([
    {
      id: "root",
      name: "Aptidão Básica",
      description: "Base para todas as habilidades.",
      unlocked: true,
      icon: "🌱",
      children: [
        {
          id: "atk1",
          name: "Ataque Rápido",
          description: "Desbloqueia ataque rápido.",
          unlocked: false,
          icon: "⚡",
        },
        {
          id: "def1",
          name: "Defesa Básica",
          description: "Desbloqueia defesa básica.",
          unlocked: false,
          icon: "🛡️",
          children: [
            {
              id: "def2",
              name: "Barreira Avançada",
              description: "Desbloqueia barreira avançada.",
              unlocked: false,
              icon: "🔰",
            },
          ],
        },
      ],
    },
  ]);

  useEffect(() => {
    fetchCharacters().then(setCharacters).finally(() => setLoading(false));
  }, []);

  function handleUnlockSkill(id: string) {
    function unlock(nodes: SkillNode[]): SkillNode[] {
      return nodes.map((n) =>
        n.id === id
          ? { ...n, unlocked: true }
          : { ...n, children: n.children ? unlock(n.children) : undefined }
      );
    }
    setSkills((prev) => unlock(prev));
  }

  if (loading) return <Loader text="Carregando personagens..." />;
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
            <CharacterForm
              onSubmit={(data) => {
                // Exemplo: adicionar personagem localmente
                if (editChar) {
                  setCharacters((chars) =>
                    chars.map((c) => (c === editChar ? data : c))
                  );
                } else {
                  setCharacters((chars) => [...chars, data]);
                }
                setShowForm(false);
              }}
              initial={editChar}
            />
          </motion.div>
        )}
        <section style={{ margin: "32px 0" }}>
          <h2>Árvore de Habilidades</h2>
          <SkillTree tree={skills} onUnlock={handleUnlockSkill} />
        </section>
        <ul>
          {characters.map((c, i) => (
            <motion.li
              key={i}
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
                onClick={() =>
                  setCharacters((chars) => chars.filter((x) => x !== c))
                }
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
            </motion.li>
          ))}
        </ul>
      </main>
    </ProtectedRoute>
  );
}
