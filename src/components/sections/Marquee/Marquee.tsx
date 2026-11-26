import styles from './marquee.module.scss'

export type MarqueeProps = {
  messages?: string[]
  /** Seconds for one full loop; lower is faster. */
  speed?: number
}

const COPIES = 4

/** Full-width strip of promo messages that scrolls continuously. */
export default function Marquee({ messages = [], speed = 40 }: MarqueeProps) {
  const items = messages.filter(Boolean)

  if (items.length === 0) {
    return null
  }

  const text = `${items.join(' - ')} - `

  return (
    <section
      className={`section ${styles.marquee}`}
      aria-label={items.join('. ')}
    >
      <div data-marquee-track style={{ animationDuration: `${speed}s` }}>
        {/* Two identical halves so translating by -50% loops seamlessly */}
        {[0, 1].map((half) => (
          <span key={half} data-marquee-half aria-hidden="true">
            {Array.from({ length: COPIES }, (_, i) => (
              <span key={i} data-marquee-item>
                {text}
              </span>
            ))}
          </span>
        ))}
      </div>
    </section>
  )
}
