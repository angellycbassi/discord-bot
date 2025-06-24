import { useState, useEffect } from "react";

export default function Loader({ text = "Carregando..." }) {
  const [dots, setDots] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => setDots((d) => (d + 1) % 4), 400);
    return () => clearInterval(interval);
  }, []);
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: 32,
      }}
    >
      <svg
        width="48"
        height="48"
        viewBox="0 0 50 50"
        style={{ marginBottom: 16 }}
        aria-hidden="true"
      >
        <circle
          cx="25"
          cy="25"
          r="20"
          fill="none"
          stroke="var(--accent)"
          strokeWidth="5"
          strokeDasharray="90 150"
          strokeLinecap="round"
        >
          <animateTransform
            attributeName="transform"
            type="rotate"
            from="0 25 25"
            to="360 25 25"
            dur="1s"
            repeatCount="indefinite"
          />
        </circle>
      </svg>
      <span
        style={{
          fontSize: 20,
          color: "var(--accent)",
          fontWeight: 500,
        }}
      >
        {text + ".".repeat(dots)}
      </span>
      <style jsx>{`
        div {
          animation: fadeIn 0.7s;
        }
        svg {
          filter: drop-shadow(0 0 8px var(--accent));
        }
      `}</style>
    </div>
  );
}
