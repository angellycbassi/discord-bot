import React, { useRef } from "react";
import { motion } from "framer-motion";

export interface SkillNode {
  id: string;
  name: string;
  description: string;
  unlocked: boolean;
  children?: SkillNode[];
  icon?: string;
}

interface SkillTreeProps {
  tree: SkillNode[];
  onUnlock: (id: string) => void;
}

export default function SkillTree({ tree, onUnlock }: SkillTreeProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 32 }}>
      {tree.map((node) => (
        <SkillBranch key={node.id} node={node} onUnlock={onUnlock} />
      ))}
    </div>
  );
}

function SkillBranch({ node, onUnlock }: { node: SkillNode; onUnlock: (id: string) => void }) {
  const buttonId = `skill-btn-${node.id}`;
  const descId = `skill-desc-${node.id}`;
  const liveRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLSpanElement>(null);

  // Função para feedback sonoro/visual ao desbloquear
  const handleUnlock = (id: string) => {
    // Corrige: não usar variáveis antes da declaração
    onUnlock(id);
    if (liveRef.current) {
      liveRef.current.textContent = node.unlocked
        ? `Habilidade já desbloqueada: "${node.name}".`
        : `Habilidade "${node.name}" desbloqueada!`;
      setTimeout(() => {
        if (liveRef.current) liveRef.current.textContent = "";
      }, 2000);
    }
  };

  // Tooltip handlers
  const showTooltip = () => {
    if (tooltipRef.current) {
      tooltipRef.current.style.visibility = "visible";
      tooltipRef.current.style.opacity = "1";
    }
  };
  const hideTooltip = () => {
    if (tooltipRef.current) {
      tooltipRef.current.style.visibility = "hidden";
      tooltipRef.current.style.opacity = "0";
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }} role="group" aria-labelledby={buttonId}>
      <motion.button
        id={buttonId}
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        whileHover={{ scale: 1.08 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => handleUnlock(node.id)}
        disabled={node.unlocked}
        tabIndex={0}
        style={{
          background: node.unlocked ? "var(--accent)" : "var(--background-secondary)",
          color: node.unlocked ? "#fff" : "var(--text)",
          border: `2px solid var(--accent)`,
          borderRadius: 16,
          padding: 16,
          minWidth: 120,
          minHeight: 60,
          marginBottom: 8,
          fontWeight: 600,
          fontSize: 16,
          boxShadow: node.unlocked ? "0 0 16px var(--accent)" : "0 2px 8px #0002",
          cursor: node.unlocked ? "default" : "pointer",
          position: "relative",
          outline: "none",
          transition: "box-shadow 0.2s, background 0.2s, color 0.2s",
        }}
        aria-label={
          node.name +
          (node.unlocked ? " (habilidade desbloqueada)" : " (pressione Enter ou Espaço para desbloquear)")
        }
        aria-describedby={descId}
        role="button"
        aria-pressed={node.unlocked}
        title={node.description}
        onKeyDown={e => {
          if (!node.unlocked && (e.key === "Enter" || e.key === " ")) {
            handleUnlock(node.id);
          }
        }}
        onFocus={showTooltip}
        onBlur={hideTooltip}
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
      >
        {node.icon && <span style={{ fontSize: 24, marginRight: 8 }} aria-hidden="true">{node.icon}</span>}
        {node.name}
        {node.unlocked && <span style={{ position: "absolute", top: 6, right: 10, fontSize: 18 }} aria-label="Desbloqueada">✔️</span>}
        {/* Tooltip visual customizado, acessível por mouse e teclado */}
        <span
          ref={tooltipRef}
          style={{
            visibility: "hidden",
            opacity: 0,
            position: "absolute",
            left: "50%",
            bottom: "110%",
            transform: "translateX(-50%)",
            background: "var(--background-tooltip, #222)",
            color: "var(--text-tooltip, #fff)",
            padding: "6px 12px",
            borderRadius: 8,
            fontSize: 13,
            whiteSpace: "pre-line",
            zIndex: 10,
            pointerEvents: "none",
            boxShadow: "0 2px 8px #0006",
            border: "1px solid var(--accent)",
            transition: "opacity 0.2s",
          }}
          className="skill-tooltip"
          aria-live="polite"
        >
          {node.description}
        </span>
      </motion.button>
      {/* Descrição acessível e feedback sonoro/visual */}
      <span id={descId} style={{ fontSize: 13, color: "#aaa", marginBottom: 4 }}>
        {node.description}
      </span>
      <div ref={liveRef} aria-live="polite" style={{ position: "absolute", left: -9999, height: 1, width: 1, overflow: "hidden" }} />
      {node.children && node.children.length > 0 && (
        <div style={{ display: "flex", gap: 32, marginTop: 8 }} role="group" aria-label={`Sub-habilidades de ${node.name}`}> 
          {node.children.map((child) => (
            <SkillBranch key={child.id} node={child} onUnlock={onUnlock} />
          ))}
        </div>
      )}
    </div>
  );
}

// Removido event listener global para tooltip, agora controlado por foco/mouse no próprio botão
