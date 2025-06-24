import React, { useState } from "react";

interface CampaignFormProps {
  onSubmit: (data: any) => void;
  initial?: any;
}

export default function CampaignForm({ onSubmit, initial }: CampaignFormProps) {
  const [nome, setNome] = useState(initial?.nome || "");
  const [descricao, setDescricao] = useState(initial?.descricao || "");
  const [historico, setHistorico] = useState(initial?.historico || "");
  const [bannerUrl, setBannerUrl] = useState(initial?.bannerUrl || "");

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        onSubmit({ nome, descricao, historico, bannerUrl });
      }}
      style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 400, margin: "24px auto" }}
    >
      <label>
        Nome:
        <input value={nome} onChange={e => setNome(e.target.value)} required />
      </label>
      <label>
        Descrição:
        <input value={descricao} onChange={e => setDescricao(e.target.value)} required />
      </label>
      <label>
        Histórico:
        <textarea value={historico} onChange={e => setHistorico(e.target.value)} />
      </label>
      <label>
        Banner URL:
        <input value={bannerUrl} onChange={e => setBannerUrl(e.target.value)} placeholder="https://..." />
      </label>
      <button type="submit" style={{ background: "var(--accent)", color: "#fff", border: 0, borderRadius: 8, padding: 8, fontWeight: 600 }}>
        {initial ? "Salvar" : "Criar"}
      </button>
    </form>
  );
}
