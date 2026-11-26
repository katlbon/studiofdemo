import { getOverriddenSection, ProductShelfSection } from '@faststore/core'

import RetailProductCard from './RetailProductCard'

// Native ProductShelf (same CMS schema), with the retail-style product card:
// name, brand, crossed-out list price, size chips and an add-to-cart button.
const RetailProductShelf = getOverriddenSection({
  Section: ProductShelfSection,
  components: {
    __experimentalProductCard: {
      Component: RetailProductCard as never,
    },
  },
})

export default RetailProductShelf
