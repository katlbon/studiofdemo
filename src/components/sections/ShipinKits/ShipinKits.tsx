import Rail from '../../common/Rail'
import styles from './shipin-kits.module.scss'

type Kit = {
  image: string
  alt?: string
  url: string
  label?: string
}

export type ShipinKitsProps = {
  title?: string
  kits?: Kit[]
}

/** "Conseguí tu kit favorito": lifestyle photo cards with an item-count pill. */
export default function ShipinKits({ title, kits = [] }: ShipinKitsProps) {
  if (kits.length === 0) return null

  return (
    <Rail title={title} visible={4.6} className={styles.kits}>
      {kits.map((kit, index) => (
        <a key={`${kit.url}-${index}`} href={kit.url} data-kit-card>
          <img src={kit.image} alt={kit.alt ?? ''} loading="lazy" />
          {kit.label && <span data-kit-label>{kit.label}</span>}
        </a>
      ))}
    </Rail>
  )
}
