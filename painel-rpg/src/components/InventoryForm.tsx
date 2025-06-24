import React, { useState } from "react";

interface InventoryFormProps {
  onSubmit: (data: any) => void;
  initial?: any;
}

export default function InventoryForm({ onSubmit, initial }: InventoryFormProps) {
  const [nome, setNome] = useState(initial?.nome || "");
  const [categoria, setCategoria] = useState(initial?.categoria || "");
  const [quantidade, setQuantidade] = useState(initial?.quantidade || 1);
  const [raridade, setRaridade] = useState(initial?.raridade || "comum");
  const [descricao, setDescricao] = useState(initial?.descricao || "");

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        onSubmit({ nome, categoria, quantidade, raridade, descricao });
      }}
      style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 340, margin: "24px auto" }}
    >
      <label>
        Nome:
        <input value={nome} onChange={e => setNome(e.target.value)} required />
      </label>
      <label>
        Categoria:
        <input value={categoria} onChange={e => setCategoria(e.target.value)} required />
      </label>
      <label>
        Quantidade:
        <input type="number" value={quantidade} onChange={e => setQuantidade(Number(e.target.value))} min={1} />
      </label>
      <label>
        Raridade:
        <select value={raridade} onChange={e => setRaridade(e.target.value)}>
          <option value="comum">Comum</option>
          <option value="raro">Raro</option>
          <option value="épico">Épico</option>
          <option value="lendário">Lendário</option>
        </select>
      </label>
      <label>
        Descrição:
        <textarea value={descricao} onChange={e => setDescricao(e.target.value)} />
      </label>
      <button type="submit" style={{ background: "var(--accent)", color: "#fff", border: 0, borderRadius: 8, padding: 8, fontWeight: 600 }}>
        {initial ? "Salvar" : "Adicionar"}
      </button>
    </form>
  );
}
