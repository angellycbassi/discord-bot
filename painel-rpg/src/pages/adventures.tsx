import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { fetchAdventures } from "../utils/api";
import Loader from "../components/Loader";

interface Adventure {
  id: number;
  nome: string;
  status: string;
  progresso: string;
  mapa: string;
}

export default function Adventures() {
  const [adventures, setAdventures] = useState<Adventure[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchAdventures().then(setAdventures).finally(() => setLoading(false));
  }, []);
  if (loading) return <Loader text="Carregando aventuras..." />;
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Aventuras</h1>
        <ul>
          {adventures.map((a) => (
            <li key={a.id}>
              <strong>{a.nome}</strong> - {a.status} - Progresso: {a.progresso}
              <br />
              <img src={a.mapa} alt="Mapa da aventura" style={{ maxWidth: 300 }} />
            </li>
          ))}
        </ul>
        {/* Mapa interativo, botões de iniciar, registrar progresso, etc. */}
      </main>
    </ProtectedRoute>
  );
}
