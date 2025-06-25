'use client'
import { useTheme } from '../context/ThemeContext'
import { Moon, Sun } from 'lucide-react'

export default function Header() {
  const { theme, toggleTheme } = useTheme()
  return (
    <header className="flex items-center justify-between px-6 py-4 bg-header border-b border-border">
      <div className="text-xl font-bold tracking-wide">RPGium Painel</div>
      <div className="flex items-center gap-4">
        <button
          aria-label="Alternar tema"
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-muted transition-colors"
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>
        <div className="flex items-center gap-2">
          <span className="font-medium">Usuário</span>
          <img
            src="/images/avatar-placeholder.png"
            alt="Avatar"
            className="w-8 h-8 rounded-full border-2 border-primary"
          />
        </div>
      </div>
    </header>
  )
}
