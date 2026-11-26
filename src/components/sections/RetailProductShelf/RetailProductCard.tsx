import { useMemo } from 'react'
import {
  Image_unstable as Image,
  useBuyButton_unstable as useBuyButton,
  useFormattedPrice_unstable as useFormattedPrice,
  useProductLink_unstable as useProductLink,
} from '@faststore/core/experimental'

import styles from './retail-product-card.module.scss'

const SIZE_VARIANT_NAMES = ['size', 'talla', 'tamanho', 'tamaño']

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

export type RetailProductCardProps = {
  product: ProductSummary
  index: number
  buttonLabel?: string
}

function getSizes(product: ProductSummary) {
  const variants = product.isVariantOf.skuVariants?.allVariantsByName ?? {}
  const key = Object.keys(variants).find((name) =>
    SIZE_VARIANT_NAMES.includes(name.toLowerCase())
  )

  return key ? variants[key] : []
}

export default function RetailProductCard({
  product,
  index,
  buttonLabel = 'Comprar',
}: RetailProductCardProps) {
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
  const sizes = useMemo(() => getSizes(product), [product])

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
    <article className={styles.retailProductCard} data-retail-card>
      <a {...linkProps} data-retail-card-link>
        <span data-retail-card-image>
          {img && (
            <Image
              src={img.url}
              alt={img.alternateName}
              width={360}
              height={480}
              sizes="(max-width: 768px) 45vw, 22vw"
            />
          )}
        </span>
        <span data-retail-card-name>{isVariantOf.name}</span>
      </a>
      <span data-retail-card-brand>{brand.brandName ?? brand.name}</span>
      <span data-retail-card-prices>
        {hasDiscount && <s data-retail-card-list-price>{listPrice}</s>}
        <strong data-retail-card-price>{price}</strong>
        {hasDiscount && (
          <span data-retail-card-discount>
            -{Math.round((1 - offer.price / offer.listPrice) * 100)}%
          </span>
        )}
      </span>
      {sizes.length > 0 && (
        <ul data-retail-card-sizes aria-label="Sizes">
          {sizes.map((size) => (
            <li key={size}>{size}</li>
          ))}
        </ul>
      )}
      <button
        type="button"
        data-retail-card-button
        disabled={outOfStock}
        onClick={buyProps.onClick}
      >
        {outOfStock ? 'Sin stock' : buttonLabel}
        {!outOfStock && (
          <svg data-retail-card-button-icon viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
            <path
              fill="currentColor"
              d="M7 18a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm10 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4ZM5.2 4l.4 2H21l-2 8H7.4l-.3 1.5H19v2H4.6l1.1-5.3L3.4 2H1V0h4l.5 2.4L5.2 4Z"
            />
          </svg>
        )}
      </button>
    </article>
  )
}
