import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { fetchEconomy } from "../utils/api";
import Loader from "../components/Loader";

interface Economy {
  moedas: number;
  badges: string[];
  historico: string[];
}

export default function Economy() {
  const [economy, setEconomy] = useState<Economy | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchEconomy().then(setEconomy).finally(() => setLoading(false));
  }, []);
  if (loading) return <Loader text="Carregando economia..." />;
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Economia</h1>
        {economy && (
          <>
            <p>
              Moedas: <b>{economy.moedas}</b>
            </p>
            <h2>Badges</h2>
            <ul>
              {economy.badges.map((b, i) => (
                <li key={i}>{b}</li>
              ))}
            </ul>
            <h2>Histórico de Transações</h2>
            <ul>
              {economy.historico.map((h, i) => (
                <li key={i}>{h}</li>
              ))}
            </ul>
          </>
        )}
        {/* Loja, transferências, etc. */}
      </main>
    </ProtectedRoute>
  );
}
