import AnnouncementBar from './sections/AnnouncementBar/AnnouncementBar'
import BenefitsBar from './sections/BenefitsBar/BenefitsBar'
import CampaignBanner from './sections/CampaignBanner/CampaignBanner'
import CategoryRail from './sections/CategoryRail/CategoryRail'
import EditorialHero from './sections/EditorialHero/EditorialHero'
import SeoText from './sections/SeoText/SeoText'
import StudioFProductGallery from './sections/StudioFProductShelf/StudioFProductGallery'
import StudioFProductShelf from './sections/StudioFProductShelf/StudioFProductShelf'

// Keys must match "$componentKey" in cms/faststore/components/*.jsonc
const sections = {
  AnnouncementBar,
  EditorialHero,
  CategoryRail,
  CampaignBanner,
  BenefitsBar,
  SeoText,
  // Native section overrides (Studio F product card)
  ProductShelf: StudioFProductShelf,
  ProductGallery: StudioFProductGallery,
}

export default sections
