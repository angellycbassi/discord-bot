import './globals.css'
import { Inter } from 'next/font/google'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'
import Footer from '../components/Footer'
import { ThemeProvider } from '../context/ThemeContext'
import { AuthProvider } from '../context/AuthContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Painel RPGium',
  description: 'Painel web do bot RPGium',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-br" suppressHydrationWarning>
      <body className={`${inter.className} bg-background text-foreground`}>
        <ThemeProvider>
          <AuthProvider>
            <div className="flex min-h-screen flex-col">
              <Header />
              <div className="flex flex-1">
                <Sidebar />
                <main className="flex-1 p-4 bg-background">{children}</main>
              </div>
              <Footer />
            </div>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
