'use client'
import { useAuth } from '../../context/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  return (
    <div className="flex flex-col items-center justify-center gap-8">
      <img
        src="/images/banner.png"
        alt="Banner RPGium"
        className="w-full max-w-3xl rounded-lg shadow-lg"
      />
      <img
        src="/images/perfil_bot.png"
        alt="Perfil Bot"
        className="w-32 h-32 rounded-full border-4 border-primary shadow-lg"
      />
      {user && (
        <div className="flex flex-col items-center gap-2">
          <img
            src={`https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`}
            alt="Avatar"
            className="w-20 h-20 rounded-full border-4 border-primary"
          />
          <span className="text-xl font-bold">{user.username}</span>
        </div>
      )}
      {/* Aqui você pode exibir estatísticas rápidas do usuário futuramente */}
    </div>
  )
}
