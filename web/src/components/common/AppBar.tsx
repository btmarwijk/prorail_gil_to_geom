import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import styles from './AppBar.module.css'

export function AppBar() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className={styles.appbar}>
      <Link to="/" className={styles.logo}>
        {/* swap for your SVG logo or <img> */}
        <div className={styles.logoIcon}>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M3 9h12M9 3v12" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
        KabelLeiding
      </Link>

      {/* Desktop nav */}
      <nav className={styles.nav}>
        <NavLink to="/about" className={styles.navLink}>Over ons</NavLink>
        <NavLink to="/contact" className={styles.navLink}>Contact</NavLink>
        <NavLink to="/login" className={styles.navBtn}>Inloggen</NavLink>
      </nav>

      {/* Mobile hamburger */}
      <button
        className={styles.hamburger}
        onClick={() => setMenuOpen((o) => !o)}
        aria-label="Menu openen"
        aria-expanded={menuOpen}
      >
        <span /><span /><span />
      </button>

      {/* Mobile drawer */}
      {menuOpen && (
        <div className={styles.drawer}>
          <NavLink to="/about" className={styles.drawerLink} onClick={() => setMenuOpen(false)}>Over ons</NavLink>
          <NavLink to="/contact" className={styles.drawerLink} onClick={() => setMenuOpen(false)}>Contact</NavLink>
          <NavLink to="/login" className={styles.drawerBtn} onClick={() => setMenuOpen(false)}>Inloggen</NavLink>
        </div>
      )}
    </header>
  )
}