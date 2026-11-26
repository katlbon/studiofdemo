import styles from './shelf-button.module.scss'

export type ShelfButtonProps = {
  text: string
  url: string
}

/** Centered navy pill link, used under product shelves ("See more"). */
export default function ShelfButton({ text, url }: ShelfButtonProps) {
  if (!text || !url) {
    return null
  }

  return (
    <section className={`section ${styles.shelfButton}`}>
      <div className="layout__content">
        <a href={url} data-shelf-button>
          {text}
        </a>
      </div>
    </section>
  )
}
