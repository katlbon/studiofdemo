import { useState } from 'react'
import { Icon } from '@faststore/ui'
import { useCartToggleButton_unstable as useCartToggleButton } from '@faststore/core/experimental'

import { BagIcon, HeartIcon, SearchIcon, TruckIcon, UserIcon } from './icons'
import styles from './studiof-header.module.scss'

type Link = { text: string; url: string }

export type StudioFHeaderProps = {
  logo?: { src: string; alt?: string }
  links?: Link[]
  accountUrl?: string
  wishlistUrl?: string
  trackingUrl?: string
  searchPlaceholder?: string
}

/**
 * Studio F header: single row with logo, inline categories and icons
 * (search, wishlist, order tracking, account, bag). The bag opens the
 * native FastStore minicart (CartSidebar).
 */
export default function StudioFHeader({
  logo = { src: '/studiof/logo.svg', alt: 'Studio F' },
  links = [],
  accountUrl = '/account',
  wishlistUrl = '/account',
  trackingUrl = '/account',
  searchPlaceholder = 'Buscar',
}: StudioFHeaderProps) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const cartButton = useCartToggleButton()
  const count = Number(cartButton['data-items'] ?? 0)

  return (
    <header className={styles.studiofHeader}>
      <div data-header-row>
        <button
          type="button"
          data-header-burger
          aria-label="Abrir menú"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((v) => !v)}
        >
          <Icon name={menuOpen ? 'X' : 'List'} width={24} height={24} />
        </button>

        <a href="/" data-header-logo aria-label={logo.alt ?? 'Studio F'}>
          <img src={logo.src} alt={logo.alt ?? 'Studio F'} width={128} height={18} />
        </a>

        <nav data-header-nav aria-label="Categorías">
          <ul>
            {links.map((link) => (
              <li key={link.url + link.text}>
                <a href={link.url}>{link.text}</a>
              </li>
            ))}
          </ul>
        </nav>

        <div data-header-icons>
          <button type="button" aria-label="Buscar" onClick={() => setSearchOpen((v) => !v)}>
            <SearchIcon />
          </button>
          <a href={wishlistUrl} aria-label="Lista de deseos" data-header-desktop-only>
            <HeartIcon />
          </a>
          <a href={trackingUrl} aria-label="Rastrear pedido" data-header-desktop-only>
            <TruckIcon />
          </a>
          <a href={accountUrl} aria-label="Mi cuenta">
            <UserIcon />
          </a>
          <button
            type="button"
            aria-label="Bolsa de compras"
            data-header-bag
            onClick={cartButton.onClick}
            data-testid={cartButton['data-testid']}
          >
            <BagIcon />
            {count > 0 && <span data-header-count>{count}</span>}
          </button>
        </div>
      </div>

      {searchOpen && (
        <form action="/s" method="get" data-header-search role="search">
          <Icon name="MagnifyingGlass" width={18} height={18} />
          <input name="q" type="search" placeholder={searchPlaceholder} aria-label={searchPlaceholder} autoFocus />
        </form>
      )}

      {menuOpen && (
        <nav data-header-drawer aria-label="Menú">
          <ul>
            {links.map((link) => (
              <li key={'m' + link.url + link.text}>
                <a href={link.url}>
                  {link.text}
                  <Icon name="CaretRight" width={16} height={16} />
                </a>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </header>
  )
}
