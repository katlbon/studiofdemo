import { useState } from 'react'

import styles from './seo-text.module.scss'

export type SeoTextProps = {
  title?: string
  paragraphs?: string[]
  readMoreLabel?: string
  readLessLabel?: string
}

/** SEO copy block with a "Leer más" toggle, as on the reference home. */
export default function SeoText({
  title,
  paragraphs = [],
  readMoreLabel = 'Leer más',
  readLessLabel = 'Leer menos',
}: SeoTextProps) {
  const [open, setOpen] = useState(false)

  if (!title && paragraphs.length === 0) return null

  return (
    <section className={`layout__content ${styles.seoText}`}>
      {title && <h2 data-seo-title>{title}</h2>}
      <div data-seo-body data-open={open || undefined}>
        {paragraphs.map((text, index) => (
          <p key={index}>{text}</p>
        ))}
      </div>
      {paragraphs.length > 1 && (
        <button type="button" data-seo-toggle onClick={() => setOpen((v) => !v)}>
          {open ? readLessLabel : readMoreLabel}
        </button>
      )}
    </section>
  )
}
