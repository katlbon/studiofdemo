import { getOverriddenSection, ProductShelfSection } from '@faststore/core'

import StudioFProductCard from './StudioFProductCard'

// Native ProductShelf (same CMS schema) rendered with the Studio F card.
const StudioFProductShelf = getOverriddenSection({
  Section: ProductShelfSection,
  components: {
    __experimentalProductCard: {
      Component: StudioFProductCard as never,
    },
  },
})

export default StudioFProductShelf
