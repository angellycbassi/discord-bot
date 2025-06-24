import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { fetchCampaigns } from "../utils/api";
import Loader from "../components/Loader";
import CampaignBanner from "../components/CampaignBanner";
import CampaignForm from "../components/CampaignForm";

interface Campaign {
  id: number;
  nome: string;
  descricao: string;
  historico: string;
  bannerUrl?: string; // Suporte a banner customizado
}

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editCamp, setEditCamp] = useState<Campaign | null>(null);

  useEffect(() => {
    fetchCampaigns().then(setCampaigns).finally(() => setLoading(false));
  }, []);
  if (loading) return <Loader text="Carregando campanhas..." />;
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Campanhas</h1>
        <button
          onClick={() => {
            setEditCamp(null);
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
          + Criar Campanha
        </button>
        {showForm && (
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            <CampaignForm
              onSubmit={(data) => {
                if (editCamp) {
                  setCampaigns((camps) =>
                    camps.map((c) => (c === editCamp ? { ...c, ...data } : c))
                  );
                } else {
                  setCampaigns((camps) => [...camps, { ...data, id: Date.now() }]);
                }
                setShowForm(false);
              }}
              initial={editCamp}
            />
          </motion.div>
        )}
        {campaigns.map((c, idx) => (
          <motion.div
            key={c.id}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1, duration: 0.6, type: "spring" }}
            style={{ marginBottom: 32 }}
          >
            <CampaignBanner nome={c.nome} bannerUrl={c.bannerUrl || undefined} />
            <div style={{ padding: 12 }}>
              <strong>{c.nome}</strong> - {c.descricao}
              <br />
              <span>Histórico: {c.historico}</span>
              <button
                onClick={() => {
                  setEditCamp(c);
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
                onClick={() => setCampaigns((camps) => camps.filter((x) => x !== c))}
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
            </div>
          </motion.div>
        ))}
      </main>
    </ProtectedRoute>
  );
}
