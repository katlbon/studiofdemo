import { useMemo } from 'react'
import {
  Image_unstable as Image,
  useBuyButton_unstable as useBuyButton,
  useFormattedPrice_unstable as useFormattedPrice,
  useProductLink_unstable as useProductLink,
} from '@faststore/core/experimental'

import styles from './studiof-product-card.module.scss'

// Shape of the ProductSummary_product fragment fields this card reads.
type ProductSummary = {
  id: string
  sku: string
  gtin: string
  slug: string
  name: string
  unitMultiplier?: number | null
  brand: { name: string; brandName?: string }
  image: Array<{ url: string; alternateName: string }>
  isVariantOf: {
    productGroupID: string
    name: string
    skuVariants?: {
      allVariantsByName?: Record<string, string[]> | null
    } | null
  }
  additionalProperty: Array<{
    propertyID: string
    name: string
    value: unknown
    valueReference: unknown
  }>
  offers: {
    lowPrice: number
    offers: Array<{
      availability: string
      price: number
      priceWithTaxes: number
      listPrice: number
      listPriceWithTaxes: number
      quantity: number
      priceToken?: string | null
      seller: { identifier: string }
    }>
  }
}

const COLOR_VARIANT_NAMES = ['color', 'cor']

// Swatch colors for the demo catalog (Color SKU specification values).
const SWATCHES: Record<string, string> = {
  Negro: '#111111',
  Blanco: '#f4f1ea',
  Natural: '#d9c7a3',
  Vino: '#6b1f2a',
  'Azul oscuro': '#1f2b4a',
  'Azul claro': '#8fb3d9',
  Dorado: '#c9a24a',
  Plateado: '#b9bcc2',
  'Verde oliva': '#5e6b3a',
  Camel: '#b0804f',
  Rosado: '#e3a9b4',
  Beige: '#cdb89a',
}

export type StudioFProductCardProps = {
  product: ProductSummary
  index: number
}

function getColors(product: ProductSummary) {
  const variants = product.isVariantOf.skuVariants?.allVariantsByName ?? {}
  const key = Object.keys(variants).find((name) =>
    COLOR_VARIANT_NAMES.includes(name.toLowerCase())
  )

  return key ? variants[key] : []
}

/**
 * Studio F product card: 4:5 photo with discount tag and quick-add bag,
 * name, red sale price + crossed list price, and color swatches.
 */
export default function StudioFProductCard({ product, index }: StudioFProductCardProps) {
  const {
    id,
    sku,
    gtin,
    unitMultiplier,
    name: variantName,
    brand,
    isVariantOf,
    image,
    additionalProperty,
    offers: {
      offers: [offer],
    },
  } = product

  const linkProps = useProductLink({ product: product as never, selectedOffer: 0, index })
  const price = useFormattedPrice(offer.price)
  const listPrice = useFormattedPrice(offer.listPrice)
  const hasDiscount = offer.listPrice > offer.price
  const outOfStock = offer.availability !== 'https://schema.org/InStock'
  const colors = useMemo(() => getColors(product), [product])

  const buyProps = useBuyButton({
    id,
    price: offer.price,
    priceWithTaxes: offer.priceWithTaxes,
    listPrice: offer.listPrice,
    listPriceWithTaxes: offer.listPriceWithTaxes,
    seller: offer.seller,
    quantity: 1,
    priceToken: offer.priceToken,
    itemOffered: {
      sku,
      name: variantName,
      gtin,
      image,
      brand,
      isVariantOf,
      additionalProperty,
      unitMultiplier,
    },
  } as never)

  const [img] = image

  return (
    <article className={styles.studiofProductCard}>
      <div data-card-media>
        <a {...linkProps} data-card-image tabIndex={-1} aria-hidden="true">
          {img && (
            <Image
              src={img.url}
              alt={img.alternateName}
              width={400}
              height={500}
              sizes="(max-width: 768px) 50vw, 25vw"
            />
          )}
        </a>
        {hasDiscount && (
          <span data-card-discount>
            -{Math.round((1 - offer.price / offer.listPrice) * 100)}%
          </span>
        )}
        <button
          type="button"
          data-card-quick-add
          aria-label={outOfStock ? 'Agotado' : `Agregar ${isVariantOf.name} a la bolsa`}
          disabled={outOfStock}
          onClick={buyProps.onClick}
        >
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              d="M5 8h14l-1 13H6L5 8Zm4 0V6a3 3 0 0 1 6 0v2M12 12v5m-2.5-2.5h5"
            />
          </svg>
        </button>
      </div>
      <a {...linkProps} data-card-name>
        {isVariantOf.name}
      </a>
      <span data-card-prices>
        <strong data-card-price data-sale={hasDiscount || undefined}>
          {price}
        </strong>
        {hasDiscount && <s data-card-list-price>{listPrice}</s>}
      </span>
      {colors.length > 0 && (
        <ul data-card-swatches aria-label="Colores">
          {colors.map((color) => (
            <li
              key={color}
              title={color}
              style={{ background: SWATCHES[color] ?? '#ccc' }}
            />
          ))}
        </ul>
      )}
    </article>
  )
}
