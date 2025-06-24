import React, { useState } from "react";

interface CharacterFormProps {
  onSubmit: (data: any) => void;
  initial?: any;
}

export default function CharacterForm({ onSubmit, initial }: CharacterFormProps) {
  const [nome, setNome] = useState(initial?.nome || "");
  const [raca, setRaca] = useState(initial?.raca || "");
  const [classe, setClasse] = useState(initial?.classe || "");
  const [xp, setXp] = useState(initial?.xp || 0);

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        onSubmit({ nome, raca, classe, xp });
      }}
      style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 340, margin: "24px auto" }}
      aria-label="Formulário de personagem"
    >
      <label htmlFor="nome-input">Nome:
        <input id="nome-input" value={nome} onChange={e => setNome(e.target.value)} required aria-required="true" aria-label="Nome do personagem" />
      </label>
      <label htmlFor="raca-input">Raça:
        <input id="raca-input" value={raca} onChange={e => setRaca(e.target.value)} required aria-required="true" aria-label="Raça do personagem" />
      </label>
      <label htmlFor="classe-input">Classe:
        <input id="classe-input" value={classe} onChange={e => setClasse(e.target.value)} required aria-required="true" aria-label="Classe do personagem" />
      </label>
      <label htmlFor="xp-input">XP:
        <input id="xp-input" type="number" value={xp} onChange={e => setXp(Number(e.target.value))} min={0} aria-label="Experiência do personagem" />
      </label>
      <button
        type="submit"
        style={{ background: "var(--accent)", color: "#fff", border: 0, borderRadius: 8, padding: 8, fontWeight: 600 }}
        aria-label={initial ? "Salvar personagem" : "Criar personagem"}
      >
        {initial ? "Salvar" : "Criar"}
      </button>
    </form>
  );
}
