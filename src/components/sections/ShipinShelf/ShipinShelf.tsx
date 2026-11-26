import type { ComponentType } from 'react'

import RetailProductShelfSection from '../RetailProductShelf/RetailProductShelf'

// The section computes `inView` itself; its exported type still lists it
const RetailProductShelf = RetailProductShelfSection as unknown as ComponentType<
  Record<string, unknown>
>
import { SHELF_PRESETS } from './presets'
import styles from './shipin-shelf.module.scss'

type Sort =
  | 'score_desc'
  | 'price_desc'
  | 'price_asc'
  | 'orders_desc'
  | 'name_desc'
  | 'name_asc'
  | 'release_desc'
  | 'discount_desc'

export type ShipinShelfProps = {
  title?: string
  moreLabel?: string
  moreUrl?: string
  /** Products: a collection (cluster) ID, a search term, or both. */
  collection?: string
  term?: string
  sort?: Sort
  numberOfItems?: number
  promo?: {
    image?: string
    title?: string
    subtitle?: string
    ctaLabel?: string
    url?: string
    /** Full-width background image behind the whole section. */
    background?: string
  }
}

/**
 * Product shelf with Shipin's header ("Título" + "Ver más →") and an optional
 * promo card on the left (e.g. "Nuevos ingresos", "14 cuotas con Naranja").
 */
export default function ShipinShelf({
  preset = 'custom',
  ...cmsProps
}: ShipinShelfProps & { preset?: string }) {
  // CMS fields win over the preset, except empty strings from the editor
  const dropEmpty = <T extends object>(obj?: T) =>
    Object.fromEntries(
      Object.entries(obj ?? {}).filter(([, value]) => value !== '' && value != null)
    ) as Partial<T>
  const filled = dropEmpty(cmsProps)
  const {
    title,
    moreLabel = 'Ver más',
    moreUrl,
    collection,
    term = '',
    sort = 'score_desc',
    numberOfItems = 10,
    promo: cmsPromo,
  }: ShipinShelfProps = { ...SHELF_PRESETS[preset], ...filled }
  const promo = { ...SHELF_PRESETS[preset]?.promo, ...dropEmpty(cmsPromo) }

  const hasPromo = Boolean(promo?.image || promo?.title)
  const shelf = (
    <RetailProductShelf
      title=""
      numberOfItems={numberOfItems}
      itemsPerPage={promo?.image ? 3 : hasPromo ? 4 : 5}
      sort={sort}
      term={term}
      selectedFacets={
        collection ? [{ key: 'productClusterIds', value: collection }] : []
      }
      productCardConfiguration={{ showDiscountBadge: true, bordered: true }}
    />
  )

  return (
    <section
      className={`section ${styles.shipinShelf}`}
      data-shelf-promo={hasPromo}
      style={
        promo?.background
          ? { backgroundImage: `url(${promo.background})` }
          : undefined
      }
    >
      <div className="layout__content">
        {!hasPromo && (title || moreUrl) && (
          <header data-shelf-header>
            {title && <h2 data-shelf-title>{title}</h2>}
            {moreUrl && (
              <a href={moreUrl} data-shelf-more>
                {moreLabel} <span aria-hidden="true">→</span>
              </a>
            )}
          </header>
        )}
        {hasPromo ? (
          <div data-shelf-grid>
            <div
              data-shelf-promo-card
              data-has-image={Boolean(promo?.image)}
              style={
                promo?.image
                  ? { backgroundImage: `url(${promo.image})` }
                  : undefined
              }
            >
              {promo?.title && <h2 data-shelf-promo-title>{promo.title}</h2>}
              {promo?.subtitle && (
                <p data-shelf-promo-subtitle>{promo.subtitle}</p>
              )}
              {promo?.url && (
                <a href={promo.url} data-shelf-promo-cta>
                  {promo.ctaLabel || moreLabel}
                </a>
              )}
            </div>
            <div data-shelf-products>{shelf}</div>
          </div>
        ) : (
          shelf
        )}
      </div>
    </section>
  )
}
