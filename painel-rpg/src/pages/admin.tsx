import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { useState } from "react";
import NPCForm from "../components/NPCForm";
import { motion } from "framer-motion";

export default function Admin() {
  const { user } = useAuth();
  const [showNPCForm, setShowNPCForm] = useState(false);
  const [npcs, setNPCs] = useState<any[]>([]);
  if (!user?.isAdmin) return <ProtectedRoute><Navbar /><div>Acesso restrito.</div></ProtectedRoute>;
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Painel do Mestre/Admin</h1>
        <button
          onClick={() => setShowNPCForm(true)}
          style={{ marginBottom: 16, background: "var(--accent)", color: "#fff", border: 0, borderRadius: 8, padding: 8, fontWeight: 600 }}
        >
          + Adicionar NPC
        </button>
        {showNPCForm && (
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
            <NPCForm
              onSubmit={data => {
                setNPCs(npcs => [...npcs, { ...data, id: Date.now() }]);
                setShowNPCForm(false);
              }}
            />
          </motion.div>
        )}
        <ul>
          {npcs.map((npc, i) => (
            <motion.li
              key={npc.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              layout
              style={{ marginBottom: 12, background: "var(--background-secondary)", borderRadius: 8, padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}
            >
              <strong>{npc.nome}</strong> - {npc.descricao} - {npc.atributos}
            </motion.li>
          ))}
        </ul>
        <ul>
          <li>Configuração de campanhas</li>
          <li>Gestão de fichas de NPCs</li>
          <li>Rolagens secretas</li>
          <li>Gestão de eventos</li>
        </ul>
        <div style={{marginTop: 32}}>
          <b>Área exclusiva para Mestres/Admins.</b>
        </div>
      </main>
    </ProtectedRoute>
  );
}
