import styles from './top-bar.module.scss'

type TopBarLink = {
  text: string
  url: string
  linkTargetBlank?: boolean
}

export type TopBarProps = {
  links?: TopBarLink[]
}

export default function TopBar({ links = [] }: TopBarProps) {
  if (links.length === 0) {
    return null
  }

  return (
    <section className={`section ${styles.topBar}`}>
      <div className="layout__content">
        <nav aria-label="Stores">
          <ul data-top-bar-list>
            {links.map((link, index) => (
              <li key={`${link.url}-${index}`} data-top-bar-item>
                <a
                  href={link.url}
                  target={link.linkTargetBlank ? '_blank' : undefined}
                  rel={link.linkTargetBlank ? 'noopener noreferrer' : undefined}
                >
                  {link.text}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </section>
  )
}
