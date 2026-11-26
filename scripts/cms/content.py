"""Build Studio F demo CMS entries for store studio-f-demo (Content Platform)."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cp import cp
from cpfmt import encode
AUTHOR = json.load(open(os.path.expanduser('~/.vtex/session/session.json')))['login']
STORE = 'studio-f-demo'; SCHEMA = 'demofskb.studio-f-demo@1.0.1'
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
announcement = {'$componentKey': 'AnnouncementBar', '$componentTitle': 'Announcement Bar', 'autoplaySeconds': 5,
    'messages': [{'text': 'ENVÍO GRATIS por compras iguales o superiores a $250.000'}, {'text': 'BLACK SALE: hasta 35% OFF en Party Season'}, {'text': 'Recibe 20% OFF suscribiéndote a nuestro NEWSLETTER'}]}
g['sections'] = [announcement] + [s for s in g['sections'] if s['$componentKey'] not in ('TopBar', 'SearchBar', 'Alert', 'ShoppingAssistant')]

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
h['sections'] = [
    {'$componentKey': 'EditorialHero', '$componentTitle': 'Editorial Hero', 'panels': [
        {'image': {'src': IMG + 'hero-1.jpg', 'alt': 'Party Season'}, 'title': 'Party Season', 'buttonLabel': 'VER MÁS', 'url': '/studiofcatalog/ropa/vestidos'},
        {'image': {'src': IMG + 'hero-2.jpg', 'alt': 'Black Sale'}, 'title': 'Black Sale', 'buttonLabel': 'VER MÁS', 'url': '/studiofcatalog'}]},
    {'$componentKey': 'CategoryRail', '$componentTitle': 'Category Rail', 'eyebrow': 'black sale', 'items': [
        {'image': IMG + 'cat-pantalones.jpg', 'label': 'Pantalones', 'url': '/studiofcatalog/ropa/pantalones'},
        {'image': IMG + 'cat-blusas.jpg', 'label': 'Blusas', 'url': '/studiofcatalog/ropa/blusas-y-camisas'},
        {'image': IMG + 'cat-bolsos.jpg', 'label': 'Bolsos', 'url': '/studiofcatalog/accesorios/bolsos-y-carteras'},
        {'image': IMG + 'cat-vestidos.jpg', 'label': 'Vestidos', 'url': '/studiofcatalog/ropa/vestidos'},
        {'image': IMG + 'cat-jeans.jpg', 'label': 'Jeans', 'url': '/studiofcatalog/jeans'},
        {'image': IMG + 'cat-zapatos.jpg', 'label': 'Zapatos', 'url': '/studiofcatalog/zapatos'}]},
    shelf('PENSADOS PARA TI', [{'key': 'productClusterIds', 'value': '138'}]),
    {'$componentKey': 'CampaignBanner', '$componentTitle': 'Campaign Banner', 'desktopImage': IMG + 'campaign-desktop.jpg',
     'mobileImage': IMG + 'campaign-mobile.jpg', 'alt': 'Black Sale hasta 35% OFF', 'buttonLabel': 'COMPRAR', 'url': '/studiofcatalog'},
    shelf('NEW ARRIVALS', [{'key': 'category-1', 'value': 'studiofcatalog'}], sort='release_desc'),
    {'$componentKey': 'SeoText', '$componentTitle': 'SEO Text', 'title': 'BLACK SALE: Ofertas en ropa para mujer', 'readMoreLabel': 'Leer más', 'readLessLabel': 'Leer menos',
     'paragraphs': [{'text': '¡BLACK SALE llegó a Studio F Demo! Aprovecha las ofertas en ropa para mujer y descubre descuentos en referencias seleccionadas de la colección Party Season.'},
                    {'text': 'Vestidos en oferta: diseños cortos, midi y largos, ideales para diferentes planes y celebraciones.'},
                    {'text': 'Blusas, jeans, zapatos y accesorios con descuentos por tiempo limitado. Tienda de demostración: imágenes y precios de prueba.'}]},
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
