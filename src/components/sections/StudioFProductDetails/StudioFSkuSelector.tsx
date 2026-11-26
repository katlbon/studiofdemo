import { SkuSelector, type SkuSelectorProps } from '@faststore/ui'

import { SWATCHES } from '../StudioFProductShelf/swatches'

/**
 * Studio F SKU selector: colors as square swatches, sizes as text boxes
 * (FastStore infers "image" for every variation that carries an image).
 */
export default function StudioFSkuSelector(props: SkuSelectorProps) {
  const { skuPropertyName, availableVariations } = props
  const isColor = skuPropertyName.toLowerCase() === 'color'
  const options = availableVariations[skuPropertyName] ?? []

  if (isColor) {
    const withHex = options.map((option) => ({
      ...option,
      hexColor: SWATCHES[option.value] ?? '#cccccc',
    }))

    return (
      <SkuSelector
        {...props}
        variant="color"
        availableVariations={{ ...availableVariations, [skuPropertyName]: withHex }}
      />
    )
  }

  const ORDER = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
  const rank = (v: string) => (ORDER.includes(v) ? ORDER.indexOf(v) : 100 + (Number(v) || 0))
  const sorted = [...options].sort((a, b) => rank(a.value) - rank(b.value))

  return (
    <SkuSelector
      {...props}
      variant="label"
      availableVariations={{ ...availableVariations, [skuPropertyName]: sorted }}
    />
  )
}
