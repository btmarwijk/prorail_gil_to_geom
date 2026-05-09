import { Link } from 'react-router-dom'
import heroImage from '../../assets/hero.png'   // 👈 your image goes here
import styles from './Hero.module.css'

export function Hero() {
  return (
    <section className={styles.hero}>
      {/* Background image — replace hero.png in src/assets/ */}
      <img src={heroImage} alt="" className={styles.heroBg} aria-hidden />
      <div className={styles.overlay} />

      <div className={styles.content}>
        <span className={styles.badge}>
          <span className={styles.dot} />
          ProRail infrastructuur
        </span>

        <h1 className={styles.title}>
          Beheer kabelinfrastructuur{' '}
          <em className={styles.accent}>efficiënt</em>
        </h1>

        <p className={styles.subtitle}>
          Verwerk ProRail Excel-bestanden, visualiseer kabeltrajecten op de kaart
          en beheer locatiedata in één platform.
        </p>

        <div className={styles.actions}>
          <Link to="/login" className={styles.btnPrimary}>
            Inloggen
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </Link>
          <Link to="/about" className={styles.btnGhost}>Meer informatie</Link>
        </div>
      </div>
    </section>
  )
}