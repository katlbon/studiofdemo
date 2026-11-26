# Studio F replica catalog definition
TREE = {
  'Ropa': ['Vestidos', 'Blusas y camisas', 'Pantalones', 'Faldas', 'Chaquetas'],
  'Jeans': ['Bota campana', 'Bota recta'],
  'Zapatos': ['Sandalias', 'Tenis'],
  'Accesorios': ['Bolsos y carteras', 'Bisuteria'],
  'Hombre': ['Camisas', 'Pantalones hombre'],
}
BRANDS = ['Studio F', 'Studio F Man', 'Ela']
MATERIALS = ['Algodon', 'Lino', 'Satin', 'Denim', 'Cuero sintetico', 'Poliester', 'Tejido de punto', 'Metal']
FITS = ['Ajustado', 'Regular', 'Holgado', 'Oversize', 'Unico']
SIZES = ['XS', 'S', 'M', 'L', '6', '8', '10', '12', '36', '37', '38', '39', 'Unica']
COLORS = {'Negro': '#111111', 'Blanco': '#f4f1ea', 'Natural': '#d9c7a3', 'Vino': '#6b1f2a', 'Azul oscuro': '#1f2b4a',
          'Azul claro': '#8fb3d9', 'Dorado': '#c9a24a', 'Plateado': '#b9bcc2', 'Verde oliva': '#5e6b3a', 'Camel': '#b0804f',
          'Rosado': '#e3a9b4', 'Beige': '#cdb89a'}
TOP = ['XS', 'S', 'M', 'L']; NUM = ['6', '8', '10', '12']; SHOE = ['36', '37', '38', '39']; ONE = ['Unica']
# name, sub, brand, material, fit, colors, sizes, usd price (list), shape, description
PRODUCTS = [
 ('Vestido largo strapless globo', 'Vestidos', 'Studio F', 'Satin', 'Ajustado', ['Natural', 'Negro'], TOP, 99.9, 'dress', 'Vestido largo strapless con falda globo y acabado satinado, ideal para eventos de noche.'),
 ('Vestido midi con insumo en manga', 'Vestidos', 'Studio F', 'Poliester', 'Regular', ['Negro', 'Vino'], TOP, 74.9, 'dress', 'Vestido midi de silueta recta con detalle de insumo en las mangas.'),
 ('Vestido corto de lentejuelas', 'Vestidos', 'Ela', 'Poliester', 'Ajustado', ['Plateado', 'Negro'], TOP, 89.9, 'dress', 'Vestido corto con lentejuelas y escote halter para la temporada de fiestas.'),
 ('Blusa halter estampada', 'Blusas y camisas', 'Studio F', 'Satin', 'Regular', ['Natural', 'Azul oscuro'], TOP, 69.9, 'top', 'Blusa halter con top interno y estampado exclusivo.'),
 ('Camiseta bordada con brillo', 'Blusas y camisas', 'Studio F', 'Algodon', 'Regular', ['Blanco', 'Negro'], TOP, 47.9, 'top', 'Camiseta de algodon con bordado frontal y aplicaciones brillantes.'),
 ('Crop top con vivos en contraste', 'Blusas y camisas', 'Ela', 'Tejido de punto', 'Ajustado', ['Blanco', 'Rosado'], TOP, 64.9, 'top', 'Crop top tejido con vivos en color contraste.'),
 ('Pantalon palazzo de lino', 'Pantalones', 'Studio F', 'Lino', 'Holgado', ['Beige', 'Negro'], NUM, 79.9, 'pants', 'Pantalon palazzo tiro alto en mezcla de lino, fresco y fluido.'),
 ('Falda midi plisada', 'Faldas', 'Studio F', 'Poliester', 'Regular', ['Camel', 'Negro'], TOP, 59.9, 'skirt', 'Falda midi plisada con pretina elastica.'),
 ('Chaqueta de cuero sintetico', 'Chaquetas', 'Studio F', 'Cuero sintetico', 'Regular', ['Negro', 'Camel'], TOP, 119.9, 'jacket', 'Chaqueta biker en cuero sintetico con cremalleras metalicas.'),
 ('Jean campana tiro alto', 'Bota campana', 'Studio F', 'Denim', 'Ajustado', ['Azul oscuro', 'Azul claro'], NUM, 74.9, 'pants', 'Jean bota campana tiro alto con pretina ancha.'),
 ('Jean recto clasico', 'Bota recta', 'Studio F', 'Denim', 'Regular', ['Azul claro', 'Negro'], NUM, 69.9, 'pants', 'Jean bota recta de tiro medio, un basico del closet.'),
 ('Sandalia de tacon metalizada', 'Sandalias', 'Studio F', 'Cuero sintetico', 'Unico', ['Dorado', 'Plateado'], SHOE, 84.9, 'shoe', 'Sandalia de tacon alto con tiras metalizadas.'),
 ('Tenis plataforma', 'Tenis', 'Ela', 'Cuero sintetico', 'Unico', ['Blanco', 'Negro'], SHOE, 79.9, 'shoe', 'Tenis de suela plataforma con detalles en contraste.'),
 ('Bolso de hombro acolchado', 'Bolsos y carteras', 'Studio F', 'Cuero sintetico', 'Unico', ['Camel', 'Negro'], ONE, 89.9, 'bag', 'Bolso de hombro acolchado con cadena dorada.'),
 ('Aretes argolla dorados', 'Bisuteria', 'Ela', 'Metal', 'Unico', ['Dorado', 'Plateado'], ONE, 24.9, 'earring', 'Aretes de argolla gruesa con acabado brillante.'),
 ('Camisa de lino manga larga', 'Camisas', 'Studio F Man', 'Lino', 'Regular', ['Blanco', 'Azul claro'], TOP, 64.9, 'shirt', 'Camisa de lino para hombre, manga larga y cuello clasico.'),
 ('Pantalon chino slim', 'Pantalones hombre', 'Studio F Man', 'Algodon', 'Ajustado', ['Beige', 'Verde oliva'], NUM, 59.9, 'pants', 'Pantalon chino slim fit en algodon con elastano.'),
]
