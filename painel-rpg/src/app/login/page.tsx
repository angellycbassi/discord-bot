'use client'
import { useAuth } from '../../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-background">
      <img src="/images/banner.png" alt="Banner" className="w-full max-w-xl rounded-lg mb-8 shadow-lg" />
      <img src="/images/perfil_bot.png" alt="Perfil Bot" className="w-24 h-24 rounded-full border-4 border-primary shadow mb-6" />
      <h1 className="text-3xl font-bold mb-2 text-center">Bem-vindo ao Painel RPGium</h1>
      <p className="mb-8 text-muted-foreground text-center">Gerencie seu RPG com Discord de forma épica.</p>
      <button
        onClick={login}
        className="flex items-center gap-3 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold shadow hover:bg-primary/80 transition"
      >
        <img src="/images/discord-mark-white.svg" alt="Discord" className="w-6 h-6" />
        Entrar com Discord
      </button>
    </div>
  )
}
