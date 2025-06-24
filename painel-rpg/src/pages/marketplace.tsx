import React, { useEffect, useState } from "react";
import axios from "axios";
import Loader from "../components/Loader";

interface MarketItem {
  id: number;
  vendedor_id: number;
  item_nome: string;
  preco: number;
  descricao: string;
  tipo: string;
  vendido: boolean;
  comprador_id?: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Marketplace() {
  const [itens, setItens] = useState<MarketItem[]>([]);
  const [nome, setNome] = useState("");
  const [preco, setPreco] = useState(0);
  const [descricao, setDescricao] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const fetchItens = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/marketplace`);
      setItens(res.data.filter((i: MarketItem) => !i.vendido));
    } catch {
      setMsg("Erro ao carregar o mercado.");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchItens();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API_URL}/marketplace/add`, {
        vendedor_id: 1, // Substituir pelo ID real do usuário logado
        item_nome: nome,
        preco,
        descricao,
        tipo: "item",
      });
      setNome(""); setPreco(0); setDescricao("");
      setMsg("Item adicionado!");
      fetchItens();
    } catch {
      setMsg("Erro ao adicionar item.");
    }
    setLoading(false);
  };

  const handleBuy = async (item_id: number) => {
    setLoading(true);
    try {
      await axios.post(`${API_URL}/marketplace/buy`, {
        comprador_id: 2, // Substituir pelo ID real do usuário logado
        item_id,
      });
      setMsg("Compra realizada!");
      fetchItens();
    } catch {
      setMsg("Erro ao comprar item.");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 24 }}>
      <h1>Mercado de Jogadores/Itens</h1>
      <form onSubmit={handleAdd} style={{ marginBottom: 24, display: "flex", flexWrap: "wrap", gap: 8 }} aria-label="Adicionar item ao mercado">
        <input value={nome} onChange={e => setNome(e.target.value)} placeholder="Nome do item" required style={{ flex: 2, minWidth: 120 }} aria-label="Nome do item" />
        <input type="number" value={preco} onChange={e => setPreco(Number(e.target.value))} placeholder="Preço" required style={{ width: 80 }} aria-label="Preço" />
        <input value={descricao} onChange={e => setDescricao(e.target.value)} placeholder="Descrição" style={{ flex: 3, minWidth: 120 }} aria-label="Descrição" />
        <button type="submit" disabled={loading} style={{ minWidth: 100, fontWeight: 600 }} aria-busy={loading}>Adicionar</button>
      </form>
      {msg && <div role="status" aria-live="polite" style={{ marginBottom: 16, color: msg.includes("Erro") ? "#e74c3c" : "var(--accent)", fontWeight: 500 }}>{msg}</div>}
      <h2>Itens à venda</h2>
      {loading ? <Loader /> : (
        <ul style={{ padding: 0, listStyle: "none" }}>
          {itens.length === 0 && <li>Nenhum item à venda.</li>}
          {itens.map(item => (
            <li key={item.id} style={{ marginBottom: 12, border: "1px solid #ccc", borderRadius: 8, padding: 12, background: "var(--background-secondary)", display: "flex", flexDirection: "column", gap: 4 }}>
              <b>{item.item_nome}</b> — <span style={{ color: "var(--accent)", fontWeight: 600 }}>R${item.preco}</span> <br />
              <span style={{ color: "#888" }}>{item.descricao}</span>
              <button
                onClick={() => handleBuy(item.id)}
                disabled={loading}
                style={{ marginTop: 6, minWidth: 100, fontWeight: 600, background: "var(--accent)", color: "#fff", border: "none", borderRadius: 6, padding: "6px 12px", cursor: loading ? "not-allowed" : "pointer" }}
                aria-label={`Comprar ${item.item_nome} por R$${item.preco}`}
                tabIndex={0}
              >
                Comprar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
