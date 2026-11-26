import { useRef } from 'react'

import styles from './category-rail.module.scss'

type Item = { image: string; label: string; url: string }

export type CategoryRailProps = {
  title?: string
  items?: Item[]
}

/** "NEW ARRIVALS" rail: 3:4 category photos with a white label button. */
export default function CategoryRail({ title, items = [] }: CategoryRailProps) {
  const trackRef = useRef<HTMLDivElement>(null)

  if (items.length === 0) return null

  const scroll = (dir: 1 | -1) =>
    trackRef.current?.scrollBy({ left: dir * trackRef.current.clientWidth * 0.75, behavior: 'smooth' })

  return (
    <section className={styles.categoryRail}>
      {title && <h2 data-rail-title>{title}</h2>}
      <div data-rail-viewport>
        <button type="button" data-rail-arrow="prev" aria-label="Anterior" onClick={() => scroll(-1)}>
          ‹
        </button>
        <div ref={trackRef} data-rail-track>
          {items.map((item, index) => (
            <a key={`${item.url}-${index}`} href={item.url} data-rail-item>
              <img src={item.image} alt={item.label} loading="lazy" />
              <span data-rail-label>{item.label}</span>
            </a>
          ))}
        </div>
        <button type="button" data-rail-arrow="next" aria-label="Siguiente" onClick={() => scroll(1)}>
          ›
        </button>
      </div>
    </section>
  )
}
