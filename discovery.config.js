
module.exports = {
  seo: {
  "title": "Studio F Demo",
  "description": "Demo replica of Studio F built on FastStore + VTEX",
  "titleTemplate": "%s | Studio F Demo",
  "author": "Studio F Demo"
},

  // Theming
  theme: 'studiof',

  // Ecommerce Platform
  platform: 'vtex',

  // Platform specific configs for API
  api: {
    storeId: process.env.NEXT_PUBLIC_STORE_ID || "demofskb",
    workspace: 'master',
    environment: 'vtexcommercestable',
    hideUnavailableItems: true,
    incrementAddress: false,
  },

  // Default session
  session: {
    currency: {
      code: "USD",
      symbol: "$",
    },
    locale: "en-US",
    channel: '{"salesChannel":1,"regionId":""}',
    country: "USA",
    deliveryMode: null,
    addressType: null,
    postalCode: null,
    geoCoordinates: null,
    person: null,
  },

  cart: {
    id: '',
    items: [],
    messages: [],
    shouldSplitItem: true,
  },

  // Production URLs
  storeUrl: "https://demofskb.vtex.app",
  secureSubdomain: "https://demofskb.vtexcommercestable.com.br/",
  checkoutUrl: "https://demofskb.vtexcommercestable.com.br/checkout",
  loginUrl: "https://demofskb.vtexcommercestable.com.br/api/io/login",
  accountUrl: "https://demofskb.vtexcommercestable.com.br/api/io/account",

  previewRedirects: {
    home: '/',
    plp: "/studiofcatalog",
    search: "/s?q=vestido",
    pdp: "/vestido-largo-strapless-globo/p",
  },

  // Lighthouse CI
  lighthouse: {
    server: process.env.BASE_SITE_URL || 'http://localhost:3000',
    pages: {
      home: '/',
      pdp: "/vestido-largo-strapless-globo/p",
      collection: "/studiofcatalog",
    },
  },

  // E2E CI
  cypress: {
    pages: {
      home: '/',
      pdp: "/vestido-largo-strapless-globo/p",
      collection: "/studiofcatalog",
      collection_filtered: "/studiofcatalog/?category-1=studiofcatalog&brand=Studio%20F&facets=category-1%2Cbrand",
      search: "/s?q=vestido",
    },
    browser: 'electron',
  },

  analytics: {
    // https://developers.google.com/tag-platform/tag-manager/web#standard_web_page_installation,
    gtmContainerId: "",
  },

  experimental: {
  "nodeVersion": 18,
  "cypressVersion": 12
},

  contentSource: {
    type: 'CP',
    project: "studiofdemo",
  },
}
