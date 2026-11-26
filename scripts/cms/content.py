"""Build Studio F demo CMS entries for store studio-f-demo (Content Platform)."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cp import cp
from cpfmt import encode
AUTHOR = json.load(open(os.path.expanduser('~/.vtex/session/session.json')))['login']
STORE = 'studio-f-demo'; SCHEMA = 'demofskb.studio-f-demo@1.0.2'
BIND = {'schemaId': SCHEMA, 'dependencies': [{'parentSchemaId': SCHEMA, 'resolvedSchemaId': 'vtex.faststore@4.5.0', 'requestedSchemaId': 'vtex.faststore@4'}], 'bindingVersion': 1}
SRC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source-entries.json')))
def src(ct): return copy.deepcopy(SRC[ct]['plain'])
def sec(page, key): return next(s for s in page['sections'] if s['$componentKey'] == key)
IMG = 'https://cdn.jsdelivr.net/gh/katlbon/studiofdemo@main/public/studiof/'
LOGO = '/studiof/logo.svg'

# ---------------- global sections
g = src('globalSections')
nav = sec(g, 'Navbar'); cart = sec(g, 'CartSidebar'); foot = sec(g, 'Footer')
nav['logo'].update({'alt': 'Studio F', 'src': LOGO})
nav['navigation']['pageLinks'] = [
    {'url': '/studiofcatalog', 'text': 'Nuevo'}, {'url': '/studiofcatalog/ropa', 'text': 'Ropa'},
    {'url': '/studiofcatalog/jeans', 'text': 'Jeans'}, {'url': '/studiofcatalog/zapatos', 'text': 'Zapatos'},
    {'url': '/studiofcatalog/accesorios', 'text': 'Complementos'}, {'url': '/studiofcatalog/hombre', 'text': 'Hombre'},
    {'url': '/studiofcatalog/ropa/vestidos', 'text': 'Party Season'}]
nav['navigation']['regionalization']['enabled'] = False
nav['searchInput']['placeholder'] = 'Buscar'
cart.update({'title': 'Tu bolsa', 'alert': {'icon': {'alt': 'Truck', 'icon': 'Truck'}, 'text': 'Envío gratis por compras superiores a $250.000'},
             'emptyCart': {'title': 'Tu bolsa está vacía', 'buttonLabel': 'Ver productos'}})
cart['checkoutButton'].update({'label': 'Finalizar compra', 'loadingLabel': 'Cargando...'})
foot['logo'].update({'alt': 'Studio F', 'src': LOGO, 'link': {'url': '/', 'title': 'Studio F'}})
foot['incentives'] = [
    {'alt': 'Pago seguro', 'icon': 'ShieldCheck', 'title': ' ', 'firstLineText': 'Pago', 'secondLineText': 'seguro'},
    {'alt': 'Envío', 'icon': 'Truck', 'title': ' ', 'firstLineText': 'Envío gratis', 'secondLineText': 'desde $250.000'},
    {'alt': 'Devoluciones', 'icon': 'Calendar', 'title': ' ', 'firstLineText': 'Cambios', 'secondLineText': 'fáciles'}]
foot['footerLinks'] = [
    {'sectionTitle': 'Descubre Studio F', 'items': [{'url': '/', 'text': 'Nuestra marca'}, {'url': '/', 'text': 'Nuestras tiendas'}, {'url': '/', 'text': 'Trabaja con nosotros'}]},
    {'sectionTitle': 'Servicios', 'items': [{'url': '/', 'text': 'Personal shopper'}, {'url': '/', 'text': 'Rastrea tu pedido'}, {'url': '/', 'text': 'Tarjeta regalo'}]},
    {'sectionTitle': 'Soporte', 'items': [{'url': '/', 'text': 'Devoluciones y cambios'}, {'url': '/', 'text': 'Servicio al cliente'}, {'url': '/', 'text': 'Preguntas frecuentes'}]}]
foot['footerSocial']['title'] = 'Síguenos en'
if 'copyrightInfo' in foot: foot['copyrightInfo'] = '©2026 STUDIO F DEMO · TIENDA DE DEMOSTRACIÓN'
SF = 'https://studiofco.vtexassets.com/assets/vtex.file-manager-graphql/images/'
announcement = {'$componentKey': 'AnnouncementBar', '$componentTitle': 'Announcement Bar', 'autoplaySeconds': 5,
    'sideLinks': [{'text': 'Mujer', 'url': '/studiofcatalog', 'active': True}, {'text': 'Hombre', 'url': '/studiofcatalog/hombre'}],
    'messages': [{'text': 'Recibe: 20%OFF suscribiéndote a nuestro NEWSLETTER'}, {'text': 'ENVÍO GRATIS Por compras iguales o superiores a $250.000'}]}
header = {'$componentKey': 'StudioFHeader', '$componentTitle': 'Studio F Header', 'logo': {'src': LOGO, 'alt': 'Studio F'},
    'links': [{'text': 'Nuevo', 'url': '/studiofcatalog'}, {'text': 'Ropa', 'url': '/studiofcatalog/ropa'}, {'text': 'Jeans', 'url': '/studiofcatalog/jeans'},
              {'text': 'Zapatos', 'url': '/studiofcatalog/zapatos'}, {'text': 'Complementos', 'url': '/studiofcatalog/accesorios'},
              {'text': 'Ten Card', 'url': '/'}, {'text': 'Party Season', 'url': '/studiofcatalog/ropa/vestidos'}],
    'accountUrl': '/account', 'wishlistUrl': '/account', 'trackingUrl': '/account', 'searchPlaceholder': 'Buscar'}
g['sections'] = [announcement, header] + [s for s in g['sections'] if s['$componentKey'] not in ('TopBar', 'SearchBar', 'Alert', 'ShoppingAssistant', 'Navbar', 'RegionBar')]

# ---------------- home
h = src('home'); news = sec(h, 'Newsletter')
news.update({'title': 'SUSCRÍBETE A NUESTRO NEWSLETTER', 'description': 'Recibe 20% OFF en tu primera compra y entérate antes que nadie de lanzamientos y promociones.',
             'nameInputLabel': 'Nombre', 'emailInputLabel': 'Email', 'subscribeButton': 'SUSCRIBIRME', 'colorVariant': 'light', 'card': False})
news['toastSubscribe'].update({'title': '¡Listo!', 'message': 'Gracias por suscribirte.'})
def shelf(title, facets, sort='score_desc', n=8):
    s = copy.deepcopy(sec(SRC['home']['plain'], 'ProductShelf'))
    s.update({'title': title, 'selectedFacets': facets, 'sort': sort, 'numberOfItems': n, 'itemsPerPage': 4})
    return s
h['seo'].update({'title': 'Black Sale: Ofertas en ropa para mujer', 'description': 'Studio F demo: vestidos, blusas, jeans, zapatos y accesorios.'})
def banner(src, alt, url, label):
    return {'$componentKey': 'EditorialHero', '$componentTitle': 'Editorial Hero',
            'panels': [{'image': {'src': SF + src, 'alt': alt}, 'buttonLabel': label, 'url': url}]}
def bare_shelf(facets, sort='score_desc'):
    s = shelf(' ', facets, sort=sort); return s
h['sections'] = [
    banner('a5acfda2-cd23-4182-aa11-636f370cf566___2927e93900d66dcf40c4f6b583ef2adf.jpg', 'Fin de Año | Studio F', '/studiofcatalog/ropa/vestidos', 'VER MÁS'),
    banner('ae2f9f87-f1cc-4ce8-9f61-e0793588aedb___7fcfdf3df068f304e7a4d4eb45d879f6.jpg', 'Vestidos | Studio F', '/studiofcatalog/ropa/vestidos', 'VER MÁS'),
    {'$componentKey': 'CategoryRail', '$componentTitle': 'Category Rail', 'title': 'NEW ARRIVALS', 'items': [
        {'image': SF + '605825f1-683c-4d19-8469-21d22cce273f___ac9faa9b315acb54bca08a0db52dc4f5.jpg', 'label': 'Pantalones', 'url': '/studiofcatalog/ropa/pantalones'},
        {'image': SF + 'ab91d114-511c-48f7-9b83-967d80f29b07___cda93d00f699b4ec56c82d68b0f8c1bf.jpg', 'label': 'Blusas', 'url': '/studiofcatalog/ropa/blusas-y-camisas'},
        {'image': SF + '6af5d4f9-e689-4e70-acf4-fc3fe82719f7___77139323c261c8f722622446c516a832.jpg', 'label': 'Bolsos', 'url': '/studiofcatalog/accesorios/bolsos-y-carteras'},
        {'image': SF + 'fc911a38-e320-4469-bdfa-0b94a34be7b6___1ce999f96897eaf531043ceeb730cf43.jpg', 'label': 'Vestidos', 'url': '/studiofcatalog/ropa/vestidos'},
        {'image': SF + '0c38c04d-a347-4663-826d-62e01f5c5413___54fe2b39bf4369709a09efd73ca21622.jpg', 'label': 'Jeans', 'url': '/studiofcatalog/jeans'},
        {'image': SF + '2e782a3d-a80c-4851-8340-89bdf6646cb0___e2d5e20363047b7da97e6f524badd1dc.jpg', 'label': 'Zapatos', 'url': '/studiofcatalog/zapatos'}]},
    {'$componentKey': 'SectionHeading', '$componentTitle': 'Section Heading', 'title': 'Pensados para ti', 'pills': [
        {'text': 'Blusas', 'url': '/studiofcatalog/ropa/blusas-y-camisas'}, {'text': 'Jeans', 'url': '/studiofcatalog/jeans'},
        {'text': 'Vestidos', 'url': '/studiofcatalog/ropa/vestidos'}, {'text': 'Pantalones', 'url': '/studiofcatalog/ropa/pantalones'},
        {'text': 'Zapatos', 'url': '/studiofcatalog/zapatos'}]},
    bare_shelf([{'key': 'productClusterIds', 'value': '138'}]),
    {'$componentKey': 'CtaButton', '$componentTitle': 'CTA Button', 'label': 'VER TODO', 'url': '/studiofcatalog'},
    banner('ca8ffe3d-be86-46c1-9b23-2044e6c1b83b___d1081e7a729cc2efd609bedcc3714e5e.jpg', 'Black Sale | Studio F', '/studiofcatalog', 'COMPRAR'),
    bare_shelf([{'key': 'category-1', 'value': 'studiofcatalog'}], sort='release_desc'),
    {'$componentKey': 'SeoText', '$componentTitle': 'SEO Text', 'title': 'BLACK SALE: Ofertas en ropa para mujer', 'readMoreLabel': 'Leer más', 'readLessLabel': 'Leer menos',
     'paragraphs': [{'text': '¡BLACK SALE llegó a Studio F! Aprovecha las ofertas en ropa para mujer y descubre descuentos en referencias seleccionadas. Es el momento perfecto para renovar tu clóset, comprar esas prendas que tanto te gustan y disfrutar de precios especiales por tiempo limitado.'},
                    {'text': 'Durante BLACK SALE encontrarás diferentes estilos para cada ocasión: vestidos en oferta, blusas y camisas, jeans para mujer, pantalones y enterizos, zapatos y accesorios.'},
                    {'text': '¡No dejes pasar esta oportunidad! Aprovecha las promociones de BLACK SALE en Studio F, compra online tus prendas favoritas y disfruta de descuentos por tiempo limitado antes de que se agoten.'}]},
    {'$componentKey': 'BenefitsBar', '$componentTitle': 'Benefits Bar', 'items': [
        {'icon': 'ShieldCheck', 'text': 'Pago rápido y seguro con múltiples medios'}, {'icon': 'Truck', 'text': 'Envío gratis por compras mayores a $250.000'},
        {'icon': 'MapPin', 'text': 'Seguimiento en tiempo real'}, {'icon': 'ArrowsClockwise', 'text': 'Devoluciones y cambios fáciles'},
        {'icon': 'User', 'text': 'Servicio gratis de Personal Shopper'}]},
    news]

# ---------------- PLP / search
p = src('plp'); p['sections'] = [s for s in p['sections'] if s['$componentKey'] in ('Breadcrumb', 'ProductGallery')]
for s in p['sections']:
    if s['$componentKey'] == 'Breadcrumb': s['alt'] = 'Inicio'
p['productGallery'] = {'itemsPerPage': 12, '$componentTitle': 'Product Gallery', 'sortBySelection': 'release_desc'}
srch = src('search')
# ---------------- PDP
d = src('pdp'); pd = sec(d, 'ProductDetails')
pd['buyButton'] = {'icon': {'alt': 'Bolsa', 'icon': 'ShoppingCart'}, 'title': 'Añadir a la bolsa'}
pd['notAvailableButton'] = {'title': 'Agotado'}
pd['productTitle']['discountBadge'] = {'size': 'small', 'showDiscountBadge': True}
pd['shippingSimulator'].update({'title': 'Envío', 'inputLabel': 'Código postal', 'link': {'to': '/', 'text': 'No sé mi código postal'}})
pd['productDescription'].update({'title': 'Información del producto'})
cs = copy.deepcopy(sec(d, 'CrossSellingShelf')); cs.update({'title': 'COMPLETA TU LOOK', 'kind': 'buy', 'itemsPerPage': 4})
cs2 = copy.deepcopy(sec(d, 'CrossSellingShelf')); cs2.update({'title': 'TAMBIÉN TE PUEDE GUSTAR', 'kind': 'view', 'itemsPerPage': 4})
d['sections'] = [s for s in d['sections'] if s['$componentKey'] in ('Breadcrumb', 'ProductDetails')] + [cs, cs2]

PAGES = [('globalSections', 'Global Sections', g, []), ('home', 'Home', h, ['/']), ('plp', 'Product List Page', p, []),
         ('pdp', 'Product Details Page', d, []), ('search', 'Search Page', srch, []), ('500', '500 Error', src('500'), []),
         ('login', 'Login Page', src('login'), [])]
s, lst = cp('GET', f'/{STORE}/branches/main/entries'); existing = {e['contentTypeId']: e for e in lst['entries']}
only = sys.argv[1:]
for ct, name, data, kw in PAGES:
    if only and ct not in only: continue
    body = {'author': AUTHOR, 'contentTypeId': ct, 'message': f'Studio F demo: {name}', 'data': encode(data),
            'schemaBinding': BIND, 'entryName': name, 'identifierKeys': [], 'search_keywords': kw}
    if ct in existing:
        s, lv = cp('GET', f"/{STORE}/{ct}/entries/{existing[ct]['id']}/last-version?branchId=main")
        body.update({'entryId': existing[ct]['id'], 'baseHash': lv['baseHash']})
    s, r = cp('POST', f'/{STORE}/branches/main/commits', body)
    print(ct, s, r.get('entryId') if s < 300 else json.dumps(r)[:1500])
