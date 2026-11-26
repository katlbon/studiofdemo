import styles from './editorial-hero.module.scss'

type Panel = {
  image: { src: string; alt?: string }
  title?: string
  buttonLabel?: string
  url?: string
}

export type EditorialHeroProps = {
  panels?: Panel[]
}

/** Full-bleed editorial hero: two (or more) side-by-side photos with a CTA. */
export default function EditorialHero({ panels = [] }: EditorialHeroProps) {
  if (panels.length === 0) return null

  return (
    <section
      className={styles.editorialHero}
      style={{ ['--panels' as string]: panels.length }}
    >
      {panels.map((panel, index) => (
        <a key={`${panel.image.src}-${index}`} href={panel.url ?? '#'} data-hero-panel>
          <img
            src={panel.image.src}
            alt={panel.image.alt ?? ''}
            loading={index === 0 ? 'eager' : 'lazy'}
          />
          {(panel.title || panel.buttonLabel) && (
            <span data-hero-content>
              {panel.title && <span data-hero-title>{panel.title}</span>}
              {panel.buttonLabel && <span data-hero-button>{panel.buttonLabel}</span>}
            </span>
          )}
        </a>
      ))}
    </section>
  )
}
