import { getOverriddenSection, ProductGallerySection } from '@faststore/core'

import StudioFProductCard from './StudioFProductCard'

// Native PLP/search grid rendered with the Studio F card.
const StudioFProductGallery = getOverriddenSection({
  Section: ProductGallerySection,
  components: {
    __experimentalProductCard: {
      Component: StudioFProductCard as never,
    },
  },
})

export default StudioFProductGallery
