import { useRef } from 'react'
import { Image_unstable as Image } from '@faststore/core/experimental'

import styles from './category-carousel.module.scss'

type CategoryItem = {
  title: string
  image: {
    src: string
    alt?: string
  }
  link: {
    text: string
    url: string
    linkTargetBlank?: boolean
  }
}

export type CategoryCarouselProps = {
  title?: string
  items?: CategoryItem[]
}

export default function CategoryCarousel({
  title,
  items = [],
}: CategoryCarouselProps) {
  const trackRef = useRef<HTMLUListElement>(null)

  if (items.length === 0) {
    return null
  }

  // Scroll by one visible page of tiles
  const scrollPage = (direction: 1 | -1) => {
    const track = trackRef.current
    if (!track) return
    track.scrollBy({ left: direction * track.clientWidth, behavior: 'smooth' })
  }

  return (
    <section className={`section ${styles.categoryCarousel}`}>
      {title && (
        <div className="layout__content">
          <h2 data-category-carousel-title>{title}</h2>
        </div>
      )}
      <div data-category-carousel-band>
        <div className="layout__content" data-category-carousel-viewport>
          <button
            type="button"
            aria-label="Previous categories"
            data-category-carousel-arrow="prev"
            onClick={() => scrollPage(-1)}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" strokeWidth="2" />
            </svg>
          </button>
          <button
            type="button"
            aria-label="Next categories"
            data-category-carousel-arrow="next"
            onClick={() => scrollPage(1)}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" strokeWidth="2" />
            </svg>
          </button>
          <ul ref={trackRef} data-category-carousel-track>
            {items.map((item, index) => (
              <li key={`${item.title}-${index}`} data-category-carousel-item>
                <a
                  href={item.link.url}
                  target={item.link.linkTargetBlank ? '_blank' : undefined}
                  rel={item.link.linkTargetBlank ? 'noopener noreferrer' : undefined}
                  data-category-carousel-card
                >
                  <Image
                    src={item.image.src}
                    alt={item.image.alt ?? item.title}
                    width={360}
                    height={480}
                    sizes="(max-width: 768px) 45vw, 25vw"
                    data-category-carousel-image
                  />
                  <span data-category-carousel-overlay>
                    <span data-category-carousel-name>{item.title}</span>
                    <span data-category-carousel-cta>{item.link.text}</span>
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
