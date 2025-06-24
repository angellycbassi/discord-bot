import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { fetchInventory } from "../utils/api";
import Loader from "../components/Loader";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { InventoryItem, InventoryDropZone } from "../components/InventoryDragDrop";
import InventoryForm from "../components/InventoryForm";
import { motion } from "framer-motion";

interface Item {
  id: number;
  nome: string;
  categoria: string;
  quantidade: number;
  raridade: string;
  descricao: string;
}

export default function Inventory() {
  const [items, setItems] = useState<Item[]>([]);
  const [baul, setBaul] = useState<Item[]>([]); // Baú/depósito
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editItem, setEditItem] = useState<Item | null>(null);

  useEffect(() => {
    fetchInventory(1).then(setItems).finally(() => setLoading(false));
  }, []);

  // Função para mover item entre inventário e baú
  function handleDrop(item: Item, target: string) {
    if (target === "baul") {
      setItems((prev) => prev.filter((i) => i.id !== item.id));
      setBaul((prev) => [...prev, item]);
    } else {
      setBaul((prev) => prev.filter((i) => i.id !== item.id));
      setItems((prev) => [...prev, item]);
    }
  }

  if (loading) return <Loader text="Carregando inventário..." />;
  return (
    <ProtectedRoute>
      <Navbar />
      <main>
        <h1>Inventário</h1>
        <button
          onClick={() => {
            setEditItem(null);
            setShowForm(true);
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
          + Adicionar Item
        </button>
        {showForm && (
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            <InventoryForm
              onSubmit={(data) => {
                if (editItem) {
                  setItems((items) =>
                    items.map((i) =>
                      i.id === editItem.id ? { ...i, ...data } : i
                    )
                  );
                } else {
                  setItems((items) => [...items, { ...data, id: Date.now() }]);
                }
                setShowForm(false);
              }}
              initial={editItem}
            />
          </motion.div>
        )}
        <DndProvider backend={HTML5Backend}>
          <section style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
            <div style={{ flex: 1 }}>
              <h2>Inventário</h2>
              <InventoryDropZone category="inventory" onDrop={handleDrop}>
                <ul style={{ minHeight: 100 }}>
                  {items.map((item) => (
                    <InventoryItem
                      key={item.id}
                      item={item}
                      onDrop={handleDrop}
                      onEdit={() => {
                        setEditItem(item);
                        setShowForm(true);
                      }}
                      onDelete={() =>
                        setItems((items) => items.filter((i) => i.id !== item.id))
                      }
                    />
                  ))}
                </ul>
              </InventoryDropZone>
            </div>
            <div style={{ flex: 1 }}>
              <h2>Baú</h2>
              <InventoryDropZone category="baul" onDrop={handleDrop}>
                <ul style={{ minHeight: 100 }}>
                  {baul.map((item) => (
                    <InventoryItem
                      key={item.id}
                      item={item}
                      onDrop={handleDrop}
                      onEdit={() => {
                        setEditItem(item);
                        setShowForm(true);
                      }}
                      onDelete={() =>
                        setBaul((baul) => baul.filter((i) => i.id !== item.id))
                      }
                    />
                  ))}
                </ul>
              </InventoryDropZone>
            </div>
          </section>
        </DndProvider>
      </main>
    </ProtectedRoute>
  );
}
