import { useCallback, useEffect, useRef, useState } from 'react'

import styles from './shipin-hero.module.scss'

type Slide = {
  image: { src: string; alt?: string }
  url?: string
}

export type ShipinHeroProps = {
  slides?: Slide[]
  autoplaySeconds?: number
}

/** Banner carousel where the neighbouring slides peek in at the edges. */
export default function ShipinHero({
  slides = [],
  autoplaySeconds = 6,
}: ShipinHeroProps) {
  const trackRef = useRef<HTMLDivElement>(null)
  const [active, setActive] = useState(0)
  const [paused, setPaused] = useState(false)
  const count = slides.length

  const goTo = useCallback(
    (index: number) => {
      const track = trackRef.current
      const next = (index + count) % count
      const slide = track?.children[next] as HTMLElement | undefined
      if (!track || !slide) return
      track.scrollTo({
        left: slide.offsetLeft - (track.clientWidth - slide.clientWidth) / 2,
        behavior: 'smooth',
      })
    },
    [count]
  )

  useEffect(() => {
    const track = trackRef.current
    if (!track) return
    const onScroll = () => {
      const center = track.scrollLeft + track.clientWidth / 2
      let closest = 0
      Array.from(track.children).forEach((child, index) => {
        const el = child as HTMLElement
        const mid = el.offsetLeft + el.clientWidth / 2
        const best = track.children[closest] as HTMLElement
        if (Math.abs(mid - center) < Math.abs(best.offsetLeft + best.clientWidth / 2 - center)) {
          closest = index
        }
      })
      setActive(closest)
    }
    track.addEventListener('scroll', onScroll, { passive: true })
    return () => track.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    if (!autoplaySeconds || paused || count < 2) return
    const timer = window.setInterval(() => goTo(active + 1), autoplaySeconds * 1000)
    return () => window.clearInterval(timer)
  }, [active, autoplaySeconds, count, goTo, paused])

  if (count === 0) return null

  return (
    <section
      className={`section ${styles.shipinHero}`}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <div ref={trackRef} data-hero-track aria-roledescription="carousel">
        {slides.map((slide, index) => {
          const img = (
            <img
              src={slide.image.src}
              alt={slide.image.alt ?? ''}
              loading={index === 0 ? 'eager' : 'lazy'}
            />
          )
          return (
            <div
              key={`${slide.image.src}-${index}`}
              data-hero-slide
              aria-roledescription="slide"
              aria-label={`${index + 1} / ${count}`}
            >
              {slide.url ? <a href={slide.url}>{img}</a> : img}
            </div>
          )
        })}
      </div>
      {count > 1 && (
        <>
          <button type="button" data-hero-arrow="prev" aria-label="Anterior" onClick={() => goTo(active - 1)}>
            ←
          </button>
          <button type="button" data-hero-arrow="next" aria-label="Siguiente" onClick={() => goTo(active + 1)}>
            →
          </button>
          <div data-hero-dots>
            {slides.map((_, index) => (
              <button
                key={index}
                type="button"
                aria-label={`Ir al banner ${index + 1}`}
                aria-current={index === active}
                data-hero-dot
                onClick={() => goTo(index)}
              />
            ))}
          </div>
        </>
      )}
    </section>
  )
}
