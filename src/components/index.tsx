import AnnouncementBar from './sections/AnnouncementBar/AnnouncementBar'
import BenefitsBar from './sections/BenefitsBar/BenefitsBar'
import CampaignBanner from './sections/CampaignBanner/CampaignBanner'
import CategoryRail from './sections/CategoryRail/CategoryRail'
import CtaButton from './sections/CtaButton/CtaButton'
import EditorialHero from './sections/EditorialHero/EditorialHero'
import SectionHeading from './sections/SectionHeading/SectionHeading'
import SeoText from './sections/SeoText/SeoText'
import StudioFHeader from './sections/StudioFHeader/StudioFHeader'
import StudioFProductDetails from './sections/StudioFProductDetails/StudioFProductDetails'
import StudioFProductGallery from './sections/StudioFProductShelf/StudioFProductGallery'
import StudioFProductShelf from './sections/StudioFProductShelf/StudioFProductShelf'

// Keys must match "$componentKey" in cms/faststore/components/*.jsonc
const sections = {
  AnnouncementBar,
  StudioFHeader,
  SectionHeading,
  CtaButton,
  EditorialHero,
  CategoryRail,
  CampaignBanner,
  BenefitsBar,
  SeoText,
  // Native section overrides (Studio F product card)
  ProductShelf: StudioFProductShelf,
  ProductGallery: StudioFProductGallery,
  ProductDetails: StudioFProductDetails,
}

export default sections
