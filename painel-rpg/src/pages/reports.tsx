import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { fetchReports } from "../utils/api";

interface Report {
  id: number;
  titulo: string;
  conteudo: string;
}

export default function Reports() {
  const [reports, setReports] = useState<Report[]>([]);
  const [exported, setExported] = useState<string | null>(null);
  useEffect(() => {
    fetchReports().then(setReports);
  }, []);
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Relatórios</h1>
        <button
          onClick={() => {
            const csv = [
              ["Título", "Conteúdo"],
              ...reports.map((r) => [r.titulo, r.conteudo.replace(/\n/g, " ")]),
            ]
              .map((row) => row.join(","))
              .join("\n");
            setExported(csv);
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
          Exportar Logs (CSV)
        </button>
        {exported && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ marginBottom: 16 }}
          >
            <textarea
              value={exported}
              readOnly
              style={{ width: "100%", minHeight: 80 }}
            />
            <a
              href={`data:text/csv;charset=utf-8,${encodeURIComponent(exported)}`}
              download="relatorios.csv"
              style={{
                display: "inline-block",
                marginTop: 8,
                background: "#4e9cff",
                color: "#fff",
                padding: "6px 16px",
                borderRadius: 6,
                textDecoration: "none",
              }}
            >
              Baixar CSV
            </a>
          </motion.div>
        )}
        <ul>
          {reports.map((r) => (
            <motion.li
              key={r.id}
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
              <strong>{r.titulo}</strong>
              <div>{r.conteudo}</div>
            </motion.li>
          ))}
        </ul>
      </main>
    </ProtectedRoute>
  );
}
