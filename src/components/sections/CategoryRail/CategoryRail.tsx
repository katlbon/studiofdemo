import { useRef } from 'react'

import styles from './category-rail.module.scss'

type Item = { image: string; label: string; url: string }

export type CategoryRailProps = {
  eyebrow?: string
  items?: Item[]
}

/** Black category tiles with a small eyebrow text and a white button label. */
export default function CategoryRail({ eyebrow, items = [] }: CategoryRailProps) {
  const trackRef = useRef<HTMLDivElement>(null)

  if (items.length === 0) return null

  const scroll = (dir: 1 | -1) =>
    trackRef.current?.scrollBy({ left: dir * trackRef.current.clientWidth * 0.75, behavior: 'smooth' })

  return (
    <section className={styles.categoryRail}>
      <button type="button" data-rail-arrow="prev" aria-label="Anterior" onClick={() => scroll(-1)}>
        ‹
      </button>
      <div ref={trackRef} data-rail-track>
        {items.map((item, index) => (
          <a key={`${item.url}-${index}`} href={item.url} data-rail-item>
            <img src={item.image} alt="" loading="lazy" />
            <span data-rail-caption>
              {eyebrow && <span data-rail-eyebrow>{eyebrow}</span>}
              <span data-rail-label>{item.label}</span>
            </span>
          </a>
        ))}
      </div>
      <button type="button" data-rail-arrow="next" aria-label="Siguiente" onClick={() => scroll(1)}>
        ›
      </button>
    </section>
  )
}
