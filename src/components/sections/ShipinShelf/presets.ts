import type { ShipinShelfProps } from './ShipinShelf'

const ASSETS = 'https://mundofixar.vtexassets.com/assets/vtex.file-manager-graphql/images'

/**
 * Ready-made Shipin home shelves, picked from a dropdown in the CMS so the
 * demo needs no manual typing. "custom" uses only the fields set in the CMS.
 */
export const SHELF_PRESETS: Record<string, Partial<ShipinShelfProps>> = {
  'nuevos-ingresos': {
    sort: 'release_desc',
    promo: {
      image: `${ASSETS}/a862644e-25e8-4bbb-93d8-fa844106a3b6___a104672bcd2d0a1d5896b15e276bd7d6.png`,
      ctaLabel: 'Ver más',
      url: '/s?sort=release_desc',
    },
  },
  naranja: {
    sort: 'discount_desc',
    promo: {
      title: '14 cuotas con Naranja',
      subtitle: '¡Y sin interés!',
      ctaLabel: 'Ver más',
      url: '/s?sort=discount_desc',
      background: `${ASSETS}/d6f7b813-bc48-4693-87d6-afb9dd2c9b96___b1de9b4dff27119b6583d3400658428f.webp`,
    },
  },
  gamer: {
    sort: 'orders_desc',
    promo: {
      image: `${ASSETS}/15d45110-8b8f-46ed-8ab8-34249c10cafe___c724d9e1a50db0df39ceae23fe1131d7.png`,
      ctaLabel: 'Ver más',
      url: '/s?sort=orders_desc',
    },
  },
  'xp-pen': {
    sort: 'price_desc',
    promo: {
      image: `${ASSETS}/1c16e9b6-cb5a-4dfa-b26e-9e280f0d4fc1___58ebc77d15b36eeb0f649c3ace2829a0.png`,
      ctaLabel: 'Ver más',
      url: '/s?sort=price_desc',
    },
  },
  cecotec: {
    title: 'Equipá tu hogar con la tecnología de Cecotec',
    moreUrl: '/s',
    sort: 'score_desc',
  },
  computadora: {
    title: 'Equipá tu computadora',
    moreUrl: '/s',
    sort: 'price_asc',
  },
  aiper: {
    title: 'Tu pileta impecable con Aiper',
    moreUrl: '/s',
    sort: 'name_asc',
  },
  cocina: {
    title: 'Cociná con estilo',
    moreUrl: '/s',
    sort: 'name_desc',
  },
}
