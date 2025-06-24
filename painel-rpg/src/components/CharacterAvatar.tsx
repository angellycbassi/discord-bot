import React, { useEffect, useRef, useState } from "react";
import Loader from "./Loader";
import axios from "axios";

interface CharacterAvatarProps {
  characterId: number;
  avatarUrl?: string;
  onAvatarChange?: (url: string) => void;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const IA_MODELS = [
  { key: "stable-diffusion", label: "Stable Diffusion" },
  { key: "dalle", label: "DALL-E" },
  { key: "midjourney", label: "Midjourney" },
];
const IA_PRESETS = [
  "guerreiro medieval, armadura dourada, fundo de floresta",
  "feiticeira cyberpunk, cabelos azuis, fundo neon",
  "anão da floresta, machado, fundo verde",
  "elfo arqueiro, capa esvoaçante, fundo de montanhas",
  "mago ancião, túnica roxa, fundo de biblioteca",
];

export default function CharacterAvatar({ characterId, avatarUrl, onAvatarChange }: CharacterAvatarProps) {
  const [url, setUrl] = useState(avatarUrl || "");
  const [uploading, setUploading] = useState(false);
  const [iaPrompt, setIaPrompt] = useState("");
  const [iaLoading, setIaLoading] = useState(false);
  const [iaModel, setIaModel] = useState(IA_MODELS[0].key);
  const [history, setHistory] = useState<any[]>([]);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    axios.get(`${API_URL}/characters/${characterId}/avatar/history`).then(res => setHistory(res.data));
  }, [characterId, url]);

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    const formData = new FormData();
    formData.append("file", e.target.files[0]);
    setUploading(true);
    try {
      // Supondo que a API aceite upload em /characters/{id}/avatar
      const res = await axios.post(`${API_URL}/characters/${characterId}/avatar`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUrl(res.data.url);
      onAvatarChange?.(res.data.url);
    } catch {
      alert("Erro ao enviar avatar.");
    }
    setUploading(false);
  };

  const handleUrl = async () => {
    const inputUrl = prompt("Cole a URL da imagem do avatar:");
    if (!inputUrl) return;
    setUploading(true);
    try {
      await axios.post(`${API_URL}/characters/${characterId}/avatar`, { url: inputUrl });
      setUrl(inputUrl);
      onAvatarChange?.(inputUrl);
    } catch {
      alert("Erro ao salvar avatar.");
    }
    setUploading(false);
  };

  const handleIa = async () => {
    const promptValue = iaPrompt || window.prompt("Descreva o avatar (ex: guerreiro elfo, armadura dourada, fundo de floresta):") || "";
    if (!promptValue) return;
    setIaLoading(true);
    try {
      const form = new FormData();
      form.append("prompt", promptValue);
      form.append("modelo", iaModel);
      const res = await axios.post(`${API_URL}/characters/${characterId}/avatar/ai`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUrl(res.data.url);
      onAvatarChange?.(res.data.url);
      setIaPrompt("");
    } catch {
      alert("Erro ao gerar avatar com IA.");
    }
    setIaLoading(false);
  };

  const handleRestore = async (url: string) => {
    setUploading(true);
    try {
      await axios.post(`${API_URL}/characters/${characterId}/avatar`, { url });
      setUrl(url);
      onAvatarChange?.(url);
    } catch {
      alert("Erro ao restaurar avatar.");
    }
    setUploading(false);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <img src={url || "/public/avatar_placeholder.png"} alt="Avatar do personagem" className="avatar" style={{ marginBottom: 8 }} />
      <div style={{ marginBottom: 8 }}>
        <button onClick={() => fileInput.current?.click()} disabled={uploading || iaLoading} style={{ marginRight: 8 }}>Upload</button>
        <input type="file" accept="image/*" style={{ display: "none" }} ref={fileInput} onChange={handleFile} />
        <button onClick={handleUrl} disabled={uploading || iaLoading} style={{ marginRight: 8 }}>Usar URL</button>
      </div>
      <div style={{ marginBottom: 8, display: "flex", justifyContent: "center", gap: 8 }}>
        <select value={iaModel} onChange={e => setIaModel(e.target.value)} disabled={iaLoading} style={{ minWidth: 120 }}>
          {IA_MODELS.map(m => <option key={m.key} value={m.key}>{m.label}</option>)}
        </select>
        <select value={iaPrompt} onChange={e => setIaPrompt(e.target.value)} disabled={iaLoading} style={{ minWidth: 220 }}>
          <option value="">Escolha um preset ou digite...</option>
          {IA_PRESETS.map(p => <option key={p} value={p}>{p}</option>)}
        </select>
        <input
          value={iaPrompt}
          onChange={e => setIaPrompt(e.target.value)}
          placeholder="Prompt IA (ex: mago ancião, fundo azul)"
          style={{ minWidth: 180 }}
          disabled={iaLoading}
        />
        <button onClick={handleIa} disabled={iaLoading || uploading} style={{ fontWeight: 600 }}>
          {iaLoading ? <Loader /> : "Gerar Avatar com IA"}
        </button>
      </div>
      <div style={{ marginTop: 16 }}>
        <h4>Histórico de Avatares</h4>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, justifyContent: "center" }}>
          {history.map((h, i) => (
            <div key={i} style={{ border: "1px solid #ccc", borderRadius: 8, padding: 6, background: "#222", maxWidth: 110 }}>
              <img src={h.url} alt="avatar antigo" style={{ width: 80, height: 80, borderRadius: 8, marginBottom: 4 }} />
              <div style={{ fontSize: 11, color: "#aaa" }}>{h.tipo} {h.modelo && `(${h.modelo})`}</div>
              {h.prompt && <div style={{ fontSize: 10, color: "#888" }} title={h.prompt}>{h.prompt.slice(0, 30)}...</div>}
              <div style={{ fontSize: 10, color: "#666" }}>{new Date(h.data).toLocaleString()}</div>
              <button onClick={() => handleRestore(h.url)} style={{ fontSize: 11, marginTop: 2 }}>Restaurar</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
