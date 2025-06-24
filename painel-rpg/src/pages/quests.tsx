import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { fetchQuests } from "../utils/api";
import Loader from "../components/Loader";

interface Quest {
  id: number;
  nome: string;
  progresso: string;
  recompensa: string;
  sugestao_ia?: string;
}

export default function Quests() {
  const [quests, setQuests] = useState<Quest[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchQuests().then(setQuests).finally(() => setLoading(false));
  }, []);
  if (loading) return <Loader text="Carregando missões..." />;
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Missões/Eventos</h1>
        <ul>
          {quests.map((q) => (
            <li key={q.id}>
              <strong>{q.nome}</strong> - Progresso: {q.progresso}
              <br />
              Recompensa: {q.recompensa}
              {q.sugestao_ia && <div><em>Gancho narrativo IA:</em> {q.sugestao_ia}</div>}
            </li>
          ))}
        </ul>
        {/* Progresso, ganchos IA, etc. */}
      </main>
    </ProtectedRoute>
  );
}
