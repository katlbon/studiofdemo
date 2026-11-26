import { useRef, type ReactNode } from 'react'

import styles from './rail.module.scss'

export type RailProps = {
  title?: string
  moreLabel?: string
  moreUrl?: string
  /** Cards visible at once on desktop. */
  visible?: number
  className?: string
  children: ReactNode
}

/**
 * Section shell used by the Shipin sections: title with an optional
 * "Ver más →" link, and a horizontally scrolling row with a round arrow.
 */
export default function Rail({
  title,
  moreLabel = 'Ver más',
  moreUrl,
  visible = 5,
  className = '',
  children,
}: RailProps) {
  const trackRef = useRef<HTMLDivElement>(null)

  const scroll = (direction: 1 | -1) => {
    const track = trackRef.current
    if (track) {
      track.scrollBy({ left: direction * track.clientWidth, behavior: 'smooth' })
    }
  }

  return (
    <section className={`section layout__section ${styles.rail} ${className}`}>
      <div className="layout__content">
        {(title || moreUrl) && (
          <header data-rail-header>
            {title && <h2 data-rail-title>{title}</h2>}
            {moreUrl && (
              <a href={moreUrl} data-rail-more>
                {moreLabel} <span aria-hidden="true">→</span>
              </a>
            )}
          </header>
        )}
        <div data-rail-viewport>
          <button
            type="button"
            data-rail-arrow="prev"
            aria-label="Anterior"
            onClick={() => scroll(-1)}
          >
            ←
          </button>
          <div
            ref={trackRef}
            data-rail-track
            style={{ ['--rail-visible' as string]: visible }}
          >
            {children}
          </div>
          <button
            type="button"
            data-rail-arrow="next"
            aria-label="Siguiente"
            onClick={() => scroll(1)}
          >
            →
          </button>
        </div>
      </div>
    </section>
  )
}
