import { useEffect, useState } from 'react'

import styles from './announcement-bar.module.scss'

type Message = { text: string; url?: string }

export type AnnouncementBarProps = {
  messages?: Message[]
  autoplaySeconds?: number
}

/** Black strip above the header with rotating messages and arrows. */
export default function AnnouncementBar({
  messages = [],
  autoplaySeconds = 5,
}: AnnouncementBarProps) {
  const [index, setIndex] = useState(0)
  const total = messages.length

  useEffect(() => {
    if (total < 2 || autoplaySeconds <= 0) return undefined
    const id = setInterval(() => setIndex((i) => (i + 1) % total), autoplaySeconds * 1000)

    return () => clearInterval(id)
  }, [total, autoplaySeconds])

  if (total === 0) return null

  const current = messages[index]
  const go = (step: number) => setIndex((i) => (i + step + total) % total)

  return (
    <section className={styles.announcementBar} aria-label="Anuncios">
      {total > 1 && (
        <button type="button" aria-label="Anterior" data-announcement-arrow onClick={() => go(-1)}>
          ‹
        </button>
      )}
      <p data-announcement-text aria-live="polite">
        {current.url ? <a href={current.url}>{current.text}</a> : current.text}
      </p>
      {total > 1 && (
        <button type="button" aria-label="Siguiente" data-announcement-arrow onClick={() => go(1)}>
          ›
        </button>
      )}
    </section>
  )
}
