import { Icon } from '@faststore/ui'

import styles from './benefits-bar.module.scss'

type Benefit = {
  icon: 'ShieldCheck' | 'Truck' | 'MapPin' | 'ArrowsClockwise' | 'User'
  text: string
}

export type BenefitsBarProps = {
  items?: Benefit[]
}

/** Black service bar (payment, shipping, tracking, returns, personal shopper). */
export default function BenefitsBar({ items = [] }: BenefitsBarProps) {
  if (items.length === 0) return null

  return (
    <section className={styles.benefitsBar}>
      <ul>
        {items.map((item, index) => (
          <li key={`${item.text}-${index}`}>
            <Icon name={item.icon} width={28} height={28} />
            <span>{item.text}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}
