import React from "react";
import { useDrag, useDrop } from "react-dnd";
import { motion } from "framer-motion";

interface InventoryItemProps {
  item: any;
  onDrop: (item: any, targetCategory: string) => void;
  onEdit?: () => void;
  onDelete?: () => void;
}

/**
 * InventoryItem - Item visual do inventário com drag-and-drop, edição e exclusão.
 * Acessível, animado e com ícone premium por raridade.
 * @param item Objeto do item
 * @param onDrop Função de drop
 * @param onEdit Função de edição
 * @param onDelete Função de exclusão
 */
export function InventoryItem({ item, onDrop, onEdit, onDelete }: InventoryItemProps) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "ITEM",
    item: { ...item },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  // Ícone premium por raridade
  const rarityColors: Record<string, string> = {
    comum: "#b0b0b0",
    raro: "#4e9cff",
    épico: "#a259ff",
    lendário: "#ffd700",
  };
  const icon = {
    comum: "📦",
    raro: "💎",
    épico: "🔮",
    lendário: "🏆",
  }[item.raridade?.toLowerCase()] || "🎲";

  return (
    <motion.li
      ref={drag}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      layout
      style={{
        opacity: isDragging ? 0.5 : 1,
        cursor: "grab",
        border: `2px solid ${rarityColors[item.raridade?.toLowerCase()] || 'var(--accent)'}`,
        borderRadius: 8,
        margin: 8,
        padding: 12,
        background: "var(--background-secondary)",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        display: "flex",
        alignItems: "center",
        gap: 12,
        transition: "border 0.2s, box-shadow 0.2s",
      }}
      aria-label={`${item.nome} (${item.categoria})`}
    >
      <span style={{ fontSize: 28, filter: "drop-shadow(0 0 4px var(--accent))" }}>{icon}</span>
      <div style={{ flex: 1 }}>
        <strong>{item.nome}</strong> ({item.categoria}) x{item.quantidade} - <span style={{ color: rarityColors[item.raridade?.toLowerCase()] }}>{item.raridade}</span>
        <br />
        <span style={{ fontSize: 13, color: "var(--text-secondary)" }}>{item.descricao}</span>
      </div>
      {onEdit && (
        <button
          onClick={e => {
            e.stopPropagation();
            onEdit();
          }}
          style={{ marginLeft: 8, background: "#444", color: "#fff", border: 0, borderRadius: 6, padding: "2px 8px", cursor: "pointer" }}
          aria-label="Editar item"
        >
          ✏️
        </button>
      )}
      {onDelete && (
        <button
          onClick={e => {
            e.stopPropagation();
            onDelete();
          }}
          style={{ marginLeft: 4, background: "#c00", color: "#fff", border: 0, borderRadius: 6, padding: "2px 8px", cursor: "pointer" }}
          aria-label="Excluir item"
        >
          🗑️
        </button>
      )}
    </motion.li>
  );
}

interface InventoryDropZoneProps {
  category: string;
  onDrop: (item: any, targetCategory: string) => void;
  children: React.ReactNode;
}

/**
 * InventoryDropZone - Área de drop para drag-and-drop de itens.
 * Acessível, com feedback visual e ARIA.
 * @param category Categoria alvo
 * @param onDrop Função de drop
 * @param children Itens filhos
 */
export function InventoryDropZone({ category, onDrop, children }: InventoryDropZoneProps) {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: "ITEM",
    drop: (item: any) => onDrop(item, category),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  }));

  return (
    <div
      ref={drop}
      style={{
        background: isOver ? "var(--accent-light)" : "transparent",
        border: `2px dashed var(--accent)`,
        borderRadius: 12,
        minHeight: 80,
        padding: 8,
        marginBottom: 16,
        transition: "background 0.2s",
      }}
      aria-label={`Dropzone ${category}`}
    >
      {children}
    </div>
  );
}
