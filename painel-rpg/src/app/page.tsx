export default function Dashboard() {
  return (
    <div className="flex flex-col items-center justify-center gap-8">
      <img
        src="/images/banner.png"
        alt="Banner RPGium"
        className="w-full max-w-3xl rounded-lg shadow-lg"
      />
      <img
        src="/images/logo-bot.png"
        alt="Logo Bot"
        className="w-32 h-32 rounded-full border-4 border-primary shadow-lg"
      />
      {/* Aqui você pode exibir estatísticas rápidas do usuário futuramente */}
    </div>
  )
}
