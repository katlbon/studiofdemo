import { getOverriddenSection, ProductDetailsSection } from '@faststore/core'

import StudioFSkuSelector from './StudioFSkuSelector'

// Native ProductDetails with Studio F color swatches and size boxes.
const StudioFProductDetails = getOverriddenSection({
  Section: ProductDetailsSection,
  components: {
    SkuSelector: { Component: StudioFSkuSelector },
  },
})

export default StudioFProductDetails
