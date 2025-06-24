import React, { useState } from "react";

interface NPCFormProps {
  onSubmit: (data: any) => void;
  initial?: any;
}

export default function NPCForm({ onSubmit, initial }: NPCFormProps) {
  const [nome, setNome] = useState(initial?.nome || "");
  const [descricao, setDescricao] = useState(initial?.descricao || "");
  const [atributos, setAtributos] = useState(initial?.atributos || "");

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        onSubmit({ nome, descricao, atributos });
      }}
      style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 340, margin: "24px auto" }}
    >
      <label>
        Nome:
        <input value={nome} onChange={e => setNome(e.target.value)} required />
      </label>
      <label>
        Descrição:
        <textarea value={descricao} onChange={e => setDescricao(e.target.value)} />
      </label>
      <label>
        Atributos:
        <input value={atributos} onChange={e => setAtributos(e.target.value)} placeholder="Força, Destreza, etc." />
      </label>
      <button type="submit" style={{ background: "var(--accent)", color: "#fff", border: 0, borderRadius: 8, padding: 8, fontWeight: 600 }}>
        {initial ? "Salvar" : "Adicionar"}
      </button>
    </form>
  );
}
