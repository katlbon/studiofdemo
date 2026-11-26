# studiofdemo — Studio F replica on FastStore + VTEX

Demo storefront that replicates the structure and style of
[studiof.com.co](https://www.studiof.com.co) (home, PLP, PDP) on **FastStore v4**
with a **VTEX** catalog. Forked from the `demofskb` starter so it can evolve on
its own.

| | |
|---|---|
| VTEX account | `demofskb` (trade policy 1, USD, en-US) |
| CMS (Content Platform) project | `studiofdemo` → schema `demofskb.studiofdemo@1.0.0` |
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
- **17 products / 124 SKUs**, one SKU per color × size, 2 images per color
  (test images generated locally, stored in `public/catalog/` and loaded into
  VTEX from `raw.githubusercontent.com`)
- **Seasonal collection:** `Party Season 2026` (id 138, 12 products)
- **Prices:** list = base price per SKU (USD); cost = 40%
- **Promotions:** `Black Sale - Party Season 35% OFF` (collection 138) and
  `Envio gratis compras > $60` (free shipping, like Studio F's > $250.000 COP)
- **Stock:** 50 units per SKU in warehouse `bodega-central` (Bodega Central → Main Dock)
- **Shipping:** policy `envio-domicilio` (Envío a domicilio, delivery, $7.90, 3 days,
  all US zips) linked to Main Dock

The scripts that created all of this are in [`scripts/catalog/`](scripts/catalog/).
They use your local `vtex login` session (no keys stored) and are idempotent
(ids kept in `state.json`), so a re-run only creates what is missing.

### Frontend

| Section (CMS key) | Folder in `src/components/sections` | Replicates |
|---|---|---|
| `AnnouncementBar` | `AnnouncementBar` | Black rotating strip "ENVÍO GRATIS…" |
| `EditorialHero` | `EditorialHero` | Two side-by-side full-bleed campaign photos |
| `CategoryRail` | `CategoryRail` | Black "black sale" tiles with white category button |
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
- Collection promotions only apply after the catalog index includes the collection
  (can take a while); check with `POST /api/checkout/pub/orderForms/simulation`.

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

## Pending / manual steps

- **CMS content** for `studiofdemo` (home, globalSections, plp, pdp) must exist in
  Admin → Storefront → Content. Without it the PLP fails with
  *Missing content on the CP for content type plp*.
