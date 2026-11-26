import styles from './section-heading.module.scss'

type Pill = { text: string; url: string }

export type SectionHeadingProps = {
  title: string
  pills?: Pill[]
}

/** Uppercase section title with optional category pills ("PENSADOS PARA TI"). */
export default function SectionHeading({ title, pills = [] }: SectionHeadingProps) {
  return (
    <section className={styles.sectionHeading}>
      <h2>{title}</h2>
      {pills.length > 0 && (
        <ul>
          {pills.map((pill, index) => (
            <li key={pill.url + index}>
              <a href={pill.url} data-active={index === 0 || undefined}>
                {pill.text}
              </a>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
