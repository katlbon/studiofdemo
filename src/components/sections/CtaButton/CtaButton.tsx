import styles from './cta-button.module.scss'

export type CtaButtonProps = {
  label: string
  url: string
}

/** Centered black call-to-action ("VER TODO"). */
export default function CtaButton({ label, url }: CtaButtonProps) {
  return (
    <section className={styles.ctaButton}>
      <a href={url}>{label}</a>
    </section>
  )
}
