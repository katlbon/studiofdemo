import CategoryCarousel from './sections/CategoryCarousel/CategoryCarousel'
import HeroSlider from './sections/HeroSlider/HeroSlider'
import ImageBanner from './sections/ImageBanner/ImageBanner'
import Marquee from './sections/Marquee/Marquee'
import PromoSlider from './sections/PromoSlider/PromoSlider'
import RetailProductShelf from './sections/RetailProductShelf/RetailProductShelf'
import SearchBar from './sections/SearchBar/SearchBar'
import ShelfButton from './sections/ShelfButton/ShelfButton'
import ShipinCards from './sections/ShipinCards/ShipinCards'
import ShipinHero from './sections/ShipinHero/ShipinHero'
import ShipinKits from './sections/ShipinKits/ShipinKits'
import ShipinShelf from './sections/ShipinShelf/ShipinShelf'
import ShipinTiles from './sections/ShipinTiles/ShipinTiles'
import TopBar from './sections/TopBar/TopBar'

const sections = {
  CategoryCarousel,
  HeroSlider,
  ImageBanner,
  Marquee,
  PromoSlider,
  SearchBar,
  ShelfButton,
  TopBar,
  // Shipin demo sections (keys match cms_component__shipin*.jsonc)
  ShipinHero,
  ShipinKits,
  ShipinFeaturedCategories: ShipinTiles,
  ShipinBrands: ShipinTiles,
  ShipinBankPromos: ShipinCards,
  ShipinInfoCards: ShipinCards,
  ShipinShelf,
  // Override: native ProductShelf with the retail product card
  ProductShelf: RetailProductShelf,
}

export default sections
