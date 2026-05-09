import { AppBar } from '../../components/common/AppBar'
import { Hero } from '../../components/home/Hero'

export default function HomePage() {
  return (
    <>
      <AppBar />
      <main>
        <Hero />
        {/* add more sections here: Features, About, Contact, Footer */}
      </main>
    </>
  )
}