import Rail from '../../common/Rail'
import styles from './shipin-cards.module.scss'

type Card = {
  image: string
  title?: string
  text?: string
  url?: string
}

export type ShipinCardsProps = {
  title?: string
  /** "promo": small logo + text (bank promotions). "info": big image, title, text and a button. */
  variant?: 'promo' | 'info'
  buttonLabel?: string
  cards?: Card[]
}

export default function ShipinCards({
  title,
  variant = 'promo',
  buttonLabel = 'Ver más',
  cards = [],
}: ShipinCardsProps) {
  if (cards.length === 0) return null

  return (
    <Rail
      title={title}
      visible={variant === 'info' ? 4.2 : 4}
      className={styles.cards}
    >
      {cards.map((card, index) => (
        <article key={`${card.image}-${index}`} data-card={variant}>
          <span data-card-media>
            <img src={card.image} alt="" loading="lazy" />
            {variant === 'promo' && card.title && (
              <strong data-card-title>{card.title}</strong>
            )}
          </span>
          {variant === 'info' && card.title && (
            <h3 data-card-title>{card.title}</h3>
          )}
          {card.text && <p data-card-text>{card.text}</p>}
          {variant === 'info' && card.url && (
            <a href={card.url} data-card-button>
              {buttonLabel} <span aria-hidden="true">→</span>
            </a>
          )}
        </article>
      ))}
    </Rail>
  )
}
