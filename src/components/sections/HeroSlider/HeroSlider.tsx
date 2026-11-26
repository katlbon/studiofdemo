import { Image_unstable as Image } from '@faststore/core/experimental'

import { useSlider } from '../../common/useSlider'
import styles from './hero-slider.module.scss'

type HeroSlide = {
  image: {
    src: string
    alt?: string
  }
  url?: string
}

export type HeroSliderProps = {
  slides?: HeroSlide[]
  autoplaySeconds?: number
}

export default function HeroSlider({
  slides = [],
  autoplaySeconds = 6,
}: HeroSliderProps) {
  const { trackRef, active, goTo, pauseProps } = useSlider(
    slides.length,
    autoplaySeconds * 1000
  )

  if (slides.length === 0) {
    return null
  }

  return (
    <section className={`section ${styles.heroSlider}`} {...pauseProps}>
      <div
        ref={trackRef}
        data-hero-slider-track
        aria-roledescription="carousel"
        aria-label="Highlights"
      >
        {slides.map((slide, index) => {
          const image = (
            <Image
              src={slide.image.src}
              alt={slide.image.alt ?? ''}
              width={1440}
              height={720}
              sizes="100vw"
              priority={index === 0}
              loading={index === 0 ? 'eager' : 'lazy'}
              data-hero-slider-image
            />
          )

          return (
            <div
              key={`${slide.image.src}-${index}`}
              data-hero-slider-slide
              aria-roledescription="slide"
              aria-label={`${index + 1} / ${slides.length}`}
            >
              {slide.url ? <a href={slide.url}>{image}</a> : image}
            </div>
          )
        })}
      </div>
      {slides.length > 1 && (
        <div data-hero-slider-dots>
          {slides.map((_, index) => (
            <button
              key={index}
              type="button"
              aria-label={`Go to slide ${index + 1}`}
              aria-current={index === active}
              data-hero-slider-dot
              onClick={() => goTo(index)}
            />
          ))}
        </div>
      )}
    </section>
  )
}
