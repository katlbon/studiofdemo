import { Image_unstable as Image } from '@faststore/core/experimental'

import { useSlider } from '../../common/useSlider'
import styles from './promo-slider.module.scss'

type PromoSlide = {
  image: {
    src: string
    alt?: string
  }
  eyebrow?: string
  title: string
  highlight?: string
  link?: {
    text: string
    url: string
  }
}

export type PromoSliderProps = {
  slides?: PromoSlide[]
  autoplaySeconds?: number
}

/** Dark promo banner slider: photo with eyebrow, title, big highlight and CTA. */
export default function PromoSlider({
  slides = [],
  autoplaySeconds = 7,
}: PromoSliderProps) {
  const { trackRef, active, goTo, pauseProps } = useSlider(
    slides.length,
    autoplaySeconds * 1000
  )

  if (slides.length === 0) {
    return null
  }

  return (
    <section className={`section ${styles.promoSlider}`} {...pauseProps}>
      <div className="layout__content">
        <div ref={trackRef} data-promo-slider-track aria-roledescription="carousel">
          {slides.map((slide, index) => (
            <article
              key={`${slide.title}-${index}`}
              data-promo-slider-slide
              aria-roledescription="slide"
              aria-label={`${index + 1} / ${slides.length}`}
            >
              <Image
                src={slide.image.src}
                alt={slide.image.alt ?? ''}
                width={1280}
                height={640}
                sizes="(max-width: 768px) 100vw, 80vw"
                data-promo-slider-image
              />
              <div data-promo-slider-content>
                {slide.eyebrow && <p data-promo-slider-eyebrow>{slide.eyebrow}</p>}
                <h2 data-promo-slider-title>{slide.title}</h2>
                {slide.highlight && (
                  <p data-promo-slider-highlight>{slide.highlight}</p>
                )}
                {slide.link?.url && (
                  <a href={slide.link.url} data-promo-slider-cta>
                    {slide.link.text}
                  </a>
                )}
              </div>
            </article>
          ))}
        </div>
        {slides.length > 1 && (
          <div data-promo-slider-dots>
            {slides.map((_, index) => (
              <button
                key={index}
                type="button"
                aria-label={`Go to slide ${index + 1}`}
                aria-current={index === active}
                data-promo-slider-dot
                onClick={() => goTo(index)}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
