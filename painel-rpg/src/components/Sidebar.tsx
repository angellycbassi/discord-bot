'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Home, Users, Backpack, Swords, BookOpen, Calendar, ShoppingCart, Trophy, Shield } from 'lucide-react'

const navItems = [
  { href: '/', label: 'Dashboard', icon: <Home size={20} /> },
  { href: '/personagens', label: 'Personagens', icon: <Users size={20} /> },
  { href: '/inventario', label: 'Inventário', icon: <Backpack size={20} /> },
  { href: '/aventuras', label: 'Aventuras', icon: <Swords size={20} /> },
  { href: '/campanhas', label: 'Campanhas', icon: <BookOpen size={20} /> },
  { href: '/missoes', label: 'Missões/Eventos', icon: <Calendar size={20} /> },
  { href: '/economia', label: 'Economia/Loja', icon: <ShoppingCart size={20} /> },
  { href: '/ranking', label: 'Ranking', icon: <Trophy size={20} /> },
  { href: '/admin', label: 'Admin/Mestre', icon: <Shield size={20} /> },
]

export default function Sidebar() {
  const pathname = usePathname()
  return (
    <aside className="hidden md:flex flex-col w-56 bg-sidebar border-r border-border py-6 px-2 min-h-screen">
      <nav className="flex flex-col gap-2">
        {navItems.map(item => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
              pathname === item.href
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-muted'
            }`}
          >
            {item.icon}
            <span className="font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  )
}
