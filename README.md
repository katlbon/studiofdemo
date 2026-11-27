# studiofdemo — Studio F replica on FastStore + VTEX

Demo storefront that replicates the structure and style of
[studiof.com.co](https://www.studiof.com.co) (home, PLP, PDP) on **FastStore v4**
with a **VTEX** catalog. Forked from the `demofskb` starter so it can evolve on
its own.

| | |
|---|---|
| VTEX account | `demofskb` — Studio F products sold **only in trade policy 2 "Secondary"** (COP, Colombia, es-CO); storefront session uses `salesChannel: 2` |
| CMS (Content Platform) store | **Studio F Demo**, store ID `studio-f-demo` → schema `demofskb.studio-f-demo@1.0.1` |
| Catalog root category | `studiofcatalog` (id 16) → `/studiofcatalog` |
| Theme | `src/themes/studiof.scss` (`theme: 'studiof'` in `discovery.config.js`) |

```bash
yarn            # install
yarn dev        # http://localhost:3000
```

---

## What was built

### Catalog (VTEX account `demofskb`)

Category tree (mirrors the Studio F menu):

```
studiofcatalog
├── Ropa ─ Vestidos · Blusas y camisas · Pantalones · Faldas · Chaquetas
├── Jeans ─ Bota campana · Bota recta
├── Zapatos ─ Sandalias · Tenis
├── Accesorios ─ Bolsos y carteras · Bisuteria
└── Hombre ─ Camisas · Pantalones hombre
```

- **Brands:** Studio F, Studio F Man, Ela
- **Specifications** (on `studiofcatalog`, inherited by every subcategory):
  - SKU: `Color` (12 values), `Talla` (XS–L, 6–12, 36–39, Unica)
  - Product: `Material`, `Ajuste` (fit)
- **20 real Studio F products / 152 SKUs** (same names, references, composition,
  colors, sizes and product photos as studiof.com.co, loaded by `step5_real.py` from
  Studio F's public catalog API). The first 17 placeholder products (generated test
  images in `public/catalog/`) are kept but deactivated.
- **Seasonal collection:** `Party Season 2026` (id 138, 12 products)
- **Prices (COP):** Studio F-like price points ($99.900 – $479.900); list = base; cost = 40%
- **Promotions:** `Black Sale - Party Season 35% OFF` (collection 138) and
  `Envio gratis compras > $250.000` (free shipping, same threshold as Studio F)
- **Stock:** 50 units per SKU in warehouse `bodega-central` (Bodega Central → Main Dock)
- **Shipping:** policy `envio-domicilio` (Envío a domicilio, delivery, $15.900, 3 days,
  all Colombian postal codes) linked to Main Dock

The scripts that created all of this are in [`scripts/catalog/`](scripts/catalog/)
(`step1` structure → `step2` products/SKUs/images/prices/stock → `step3` collection,
promotions, shipping → `step4_cop` COP re-pricing → `step5_real` real products →
`step6_secondary` product ↔ trade policy 2 only, promotions on channel 2).
They use your local `vtex login` session (no keys stored) and are idempotent
(ids kept in `state.json`), so a re-run only creates what is missing.

### Frontend

| Section (CMS key) | Folder in `src/components/sections` | Replicates |
|---|---|---|
| `AnnouncementBar` | `AnnouncementBar` | Black 48px top bar: MUJER \| HOMBRE + rotating messages |
| `StudioFHeader` | `StudioFHeader` | Single-row header: real logo, inline categories, outline icons, bag → minicart |
| `SectionHeading` | `SectionHeading` | "PENSADOS PARA TI" title + category pills |
| `CtaButton` | `CtaButton` | Black "VER TODO" button |
| `ProductDetails` (override) | `StudioFProductDetails` | Color swatches + size boxes on the PDP |
| `EditorialHero` | `EditorialHero` | Full-width 1440×600 campaign banners with VER MÁS / COMPRAR |
| `CategoryRail` | `CategoryRail` | "NEW ARRIVALS" rail of 320×427 category photos |
| `CampaignBanner` | `CampaignBanner` | "hasta 35% OFF" campaign banner + COMPRAR |
| `BenefitsBar` | `BenefitsBar` | Black service bar (pago seguro, envío, devoluciones…) |
| `SeoText` | `SeoText` | SEO copy with "Leer más" |
| `ProductShelf` (override) | `StudioFProductShelf` | Studio F product card on shelves |
| `ProductGallery` (override) | `StudioFProductShelf` | Same card on the PLP/search grid |

The PDP uses the native `ProductDetails` section; its SKU selector is driven by
the `Color` / `Talla` SKU specifications. Minicart (`CartSidebar`) and checkout
are native FastStore → VTEX checkout.

---

## Prompts that worked (reuse for future demos)

Replace `<brand>`, `<url>`, `<account>`, `<cms-project>`, `<repo>` as needed.

### 1. Kick-off (one prompt for the whole demo)

```text
I want you to replicate an entire store and create a new repository so I can work
independently from my main one. The store to replicate is <url>, the new repository
is <repo>, and I already created a new store inside the CMS called <cms-project>,
so work inside of it. Create a new category called <brand>catalog and inside it
subcategories with a catalog that matches the reference one.

Catalog:
- Pick the reference brand and build the category tree.
- Create at least 15 products with SKUs by size and color, with images per color.
- Set up brands, product specifications (material, fit) and a seasonal collection.
- Load prices and create a promotion (e.g. % off the collection).
- Assign stock to the central warehouse and create a home delivery shipping policy.

Frontend:
- Replicate the structure and style of the reference site's home, PLP and PDP, with test images.
- Use the FastStore skills to generate sections and components.
- Connect the PDP to the size and color selector of the SKUs.
- Get the minicart and native checkout working.
- Save the prompts that worked in a README, to reuse in future demos.
```

Answers that unblocked it: account = `demofskb`; auth = **`vtex login <account>`**
(Claude uses the CLI session for catalog calls and never types keys or passwords);
repo visibility = public (so VTEX can pull images from GitHub raw URLs).

### 2. Read the reference store

```text
The reference site runs on VTEX. Read its public category tree
(/api/catalog_system/pub/category/tree/2) and look at its home, PLP and PDP in the
browser (desktop and mobile), then propose a reduced tree (5 departments,
2–5 subcategories each) under <brand>catalog.
```

### 3. Catalog by script instead of one-by-one MCP calls

```text
Write idempotent Python scripts (stdlib only) that use my `vtex login` session token
to create: categories, brands, spec groups/fields/values on the root category
(SKU: Color, Talla — product: Material, Ajuste), products, SKUs per color × size,
SKU specs, 2 images per color, activate SKUs, prices (pricing API) and stock in a
new "Bodega Central" warehouse. Keep ids in state.json so re-runs only create what
is missing. Then create the seasonal collection, a % off promotion on it, a free
shipping promotion and a home-delivery shipping policy linked to the main dock.
```

Gotchas found:
- Product spec: `POST /api/catalog/pvt/product/{id}/specification` (not `/specificationvalue`).
- SKU spec: `POST /api/catalog/pvt/stockkeepingunit/{id}/specification`.
- Pricing API: send exactly two of `basePrice`, `costPrice`, `markup`.
- Create collection promotions with `collectionsIsInclusive: true` **from the start**.
  The first version was created without it (= collection excluded) and later edits of
  that flag never took effect in checkout; recreating the promotion fixed it.
  Verify with `POST /api/checkout/pub/orderForms/simulation`.

### 4. Test images

```text
Generate test product images with Pillow: 1000×1250 JPG, warm grey background,
a garment silhouette per product type filled with the SKU color, 2 shots per
color (full + detail crop), labelled "TEST IMAGE". Put them in public/catalog,
push, and load them into VTEX from raw.githubusercontent.com. Also generate
hero, campaign and category-tile test images in public/studiof.
```

### 5. Frontend sections

```text
Use the faststore-storefront skill. Replace the previous demo sections with
<brand> ones: AnnouncementBar, EditorialHero (2-up), CategoryRail (black tiles),
CampaignBanner (desktop + mobile image), BenefitsBar, SeoText. Override
ProductShelf and ProductGallery with a <brand> card (4:5 image, -% badge,
quick-add bag, red sale price + crossed list price, color swatches).
Create a new theme src/themes/<brand>.scss: black/white, square corners, Inter,
red sale price, black full-width buy button.
Then run `faststore cms-sync --dry-run`, validate, and upload to the <cms-project> store ID.
```

### 6. Schema upload (non-interactive)

`vtex content upload-schema` asks for store ID, version and confirmation; answer
`<cms-project>`, Enter (accepts 1.0.0) and `y`. An `expect` script that sends them
one at a time works; matching every prompt in a single loop double-answers and
cancels the upload.

---

### CMS content (scripted)

[`scripts/cms/content.py`](scripts/cms/content.py) creates/updates the Studio F Demo
entries (Global Sections, Home, PLP, PDP, Search, 500, Login) through the Content
Platform manage API, reusing the native sections of the `demofskb` store
(`source-entries.json`) and adding the Studio F sections:

```bash
python3 scripts/cms/content.py              # all pages
python3 scripts/cms/content.py home pdp     # only some content types
```

It commits straight to the `main` branch of store `studio-f-demo` (published).

### 7. CMS content without clicking through the Admin

```text
Read the existing entries of my other CP store (manage API, last-version on branch
main), decode them to plain JSON, replace the sections with the <brand> ones, and
commit them to <cms-store-id> main through
POST /api/content-platform/manage/{account}/{store}/branches/main/commits.
```

Gotchas found:
- The CP **store ID** is the slug in the Admin URL (`…/stores/studio-f-demo`), not the
  display name. `contentSource.project` and the schema upload must use it.
- Manage API base: `https://api.vtexcommercestable.com.br/api/content-platform/manage/{account}`
  with `Authorization: Bearer <vtex login token>`. New entries: commit without `entryId`;
  updates: send `entryId` + current `baseHash`.
- Stored data format: every scalar is a locale `switch` (`defaultCase`), arrays are
  `{"$fnType":"array","values":{id:{…,"id","$position"}}}`. Arrays of plain strings are
  not used by FastStore schemas, so model them as arrays of objects.
- The schema validates enums: e.g. `Navbar.cartIcon.icon` and the buy-button icon only
  accept `ShoppingCart`; `Footer.incentives` needs at least 3 items.
- **FastStore v4 only copies `.svg/.json/.txt/.xml/.ico` and fonts from `public/`.**
  JPG banners are served from jsDelivr (`cdn.jsdelivr.net/gh/katlbon/studiofdemo@main/public/studiof/…`).
- FastStore buy-button tokens (`--fs-buy-button-*`) are declared on
  `[data-fs-buy-button]`, so override them on that selector, not on `.theme`.

### 8. Pixel-match the reference

```text
Open the reference and the local store side by side at 1440px. Measure with JS the
y/x/size of the top bar, header items, banners, section titles, tiles and product
cards on both, and fix spacing, fonts (Zalando Sans SemiExpanded + Inter), icons and
colors until they match. Use the reference's real logo SVG and banner images.
```

Gotchas found:
- FastStore's lazy sections leave an 823px placeholder until scrolled into view; measure
  after scrolling step by step, not with a single `scrollTo`.
- The native Navbar always renders the search box and a second link row; replace it with
  a custom header section (uses `useCartToggleButton_unstable` for the minicart).
- The PDP SKU selector shows photos for every variation that has images; override the
  `SkuSelector` slot of `ProductDetails` to force color swatches and size labels.
- Keep sticky bars at `z-index` ≤ 2: the minicart overlay is `z-index: 3`.
- New products can take several minutes to reach Intelligent Search; the PDP shows
  loading placeholders for price/buy button until they are indexed. Re-saving the
  product (`PUT /api/catalog/pvt/product/{id}`) re-queues it.

### 9. Restrict a catalog to one trade policy

```text
Associate the <brand> products only with trade policy 2 "Secondary", point the
storefront session at salesChannel 2 and move the promotions to channel 2. Verify
with cart simulation on sc=1 (not sellable) and sc=2 (sellable, promo, shipping).
```

Gotchas found:
- `POST /api/catalog/pvt/product/{id}/salespolicy/{tradePolicyId}`; with no association the
  product is only served on the main policy.
- Intelligent Search filters by `trade-policy/<id>`; re-save each product
  (`PUT /api/catalog/pvt/product/{id}`) so it is reindexed under the new policy.
- Editing `idsSalesChannel` on an existing promotion did not reach checkout; recreate the
  promotion on the new channel and deactivate the old one.
- The dock must list the new sales channel (`Main Dock` → `["1","2"]`).

### 10. Verify like a shopper

```text
Run the store locally and check home, PLP and PDP against the reference. On the PDP
change color and size and confirm the SKU, images and URL change; add to the bag,
open the minicart and go to the native checkout; calculate shipping for Bogotá.
```

---

## Status / known gaps

- Verified locally: home, PLP (`/studiofcatalog`), PDP color/size selector, minicart,
  native checkout with "Envío a domicilio" for Bogotá (free over $250.000).
- Prices were re-loaded in COP after the trade policy changed from USD to COP; the
  search index refreshes them asynchronously, so shelves/PLP may show old values
  until Intelligent Search reindexes (checkout already uses the new prices).
- 35% Party Season promotion verified in cart simulation (e.g. Blusa halter
  $279.900 → $181.935; items outside the collection keep full price).
- **WebOps:** the account's WebOps project (Admin → Storefront → FastStore WebOps →
  Integrations) is connected to this repo; each push to `main` deploys. The CMS store's
  build settings (Admin → Content → Stores → Studio F Demo) should point at the WebOps
  preview URL so CMS previews open this storefront.
