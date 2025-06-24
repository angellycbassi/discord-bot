import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const themes = [
    { key: "dark", label: "🌙" },
    { key: "light", label: "☀️" },
    { key: "medieval", label: "🛡️" },
    { key: "cyberpunk", label: "🦾" },
    { key: "forest", label: "🌲" },
  ];
  const [theme, setTheme] = useState("dark");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  function nextTheme() {
    const idx = themes.findIndex((t) => t.key === theme);
    setTheme(themes[(idx + 1) % themes.length].key);
  }

  return (
    <button className="theme-toggle" onClick={nextTheme} title="Alternar tema">
      {themes.find((t) => t.key === theme)?.label}
    </button>
  );
}
