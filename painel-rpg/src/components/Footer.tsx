export default function Footer() {
  return (
    <footer className="w-full py-3 px-6 bg-footer border-t border-border text-center text-xs text-muted-foreground">
      © {new Date().getFullYear()} RPGium. Todos os direitos reservados.
    </footer>
  )
}
