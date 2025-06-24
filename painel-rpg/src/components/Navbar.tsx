import Link from "next/link";
import { useAuth } from "../context/AuthContext";
import ThemeToggle from "./ThemeToggle";

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <nav className="navbar" role="navigation" aria-label="Navegação principal">
      <Link href="/" aria-label="Página inicial do RPGium"><b>RPGium</b></Link>
      <div>
        <Link href="/characters" aria-label="Ir para Personagens">Personagens</Link>
        <Link href="/inventory" aria-label="Ir para Inventário">Inventário</Link>
        <Link href="/adventures" aria-label="Ir para Aventuras">Aventuras</Link>
        <Link href="/campaigns" aria-label="Ir para Campanhas">Campanhas</Link>
        <Link href="/quests" aria-label="Ir para Missões">Missões</Link>
        <Link href="/economy" aria-label="Ir para Economia">Economia</Link>
        <Link href="/reports" aria-label="Ir para Relatórios">Relatórios</Link>
        {user?.isAdmin && <Link href="/admin" aria-label="Ir para Admin">Admin</Link>}
        <a
          href="https://discord.com/invite/seu-servidor"
          target="_blank"
          rel="noopener noreferrer"
          title="Acesse o Discord (abre em nova aba)"
          aria-label="Acesse o Discord (abre em nova aba)"
          style={{ display: "inline-flex", alignItems: "center", gap: 4 }}
        >
          <img src="/assets/discord.svg" alt="Discord" style={{ width: 28, verticalAlign: 'middle' }} />
          <span className="sr-only">Discord</span>
        </a>
        {user && (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              marginLeft: 12,
              fontWeight: 500,
              color: "var(--accent)",
              background: "var(--background-secondary)",
              borderRadius: 8,
              padding: "2px 10px",
              fontSize: 15,
              boxShadow: "0 1px 4px #0002"
            }}
            title={user.username}
            aria-label={`Usuário logado: ${user.username}`}
            tabIndex={0}
          >
            <img
              src={user.avatar || "/assets/discord.svg"}
              alt="Avatar Discord"
              style={{ width: 24, height: 24, borderRadius: "50%", marginRight: 6 }}
            />
            {user.username}
          </span>
        )}
        <ThemeToggle />
        <button onClick={logout} aria-label="Sair da conta" title="Sair" tabIndex={0}>Sair</button>
      </div>
      <style jsx>{`
        .navbar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          background: var(--secondary-bg);
          padding: 1rem 2rem;
          border-radius: 0 0 16px 16px;
          margin-bottom: 2rem;
        }
        .navbar a, .navbar button {
          color: var(--text);
          margin-left: 1rem;
          background: none;
          border: none;
          cursor: pointer;
          font-size: 1rem;
        }
        .navbar a:focus, .navbar button:focus {
          outline: 2px solid var(--accent);
          outline-offset: 2px;
        }
        .navbar a:hover, .navbar button:hover {
          color: var(--accent);
        }
      `}</style>
    </nav>
  );
}
