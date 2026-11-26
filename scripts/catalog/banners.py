import os, sys, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
F = '/System/Library/Fonts/Helvetica.ttc'
def font(s, bold=True):
    try: return ImageFont.truetype(F, s, index=1 if bold else 0)
    except Exception: return ImageFont.load_default()
def bokeh(w, h, seed, base=(12, 12, 16), tint=(255, 220, 170)):
    random.seed(seed)
    im = Image.new('RGB', (w, h), base); glow = Image.new('RGB', (w, h), (0, 0, 0)); d = ImageDraw.Draw(glow)
    for _ in range(int(w * h / 9000)):
        x, y, r = random.randint(0, w), random.randint(0, int(h * .75)), random.randint(4, 26)
        k = random.uniform(.25, 1); c = tuple(int(v * k) for v in (tint if random.random() < .7 else (180, 200, 255)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    glow = glow.filter(ImageFilter.GaussianBlur(5))
    return Image.blend(im, glow, .55)
def figure(im, cx, scale, color=(20, 20, 24), sequin=True):
    w, h = im.size; d = ImageDraw.Draw(im)
    s = scale
    # head + hair
    d.ellipse((cx - 55 * s, h * .18, cx + 55 * s, h * .18 + 135 * s), fill=(60, 45, 38))
    d.ellipse((cx - 42 * s, h * .18 + 25 * s, cx + 42 * s, h * .18 + 125 * s), fill=(196, 160, 138))
    neck = h * .18 + 120 * s
    d.rectangle((cx - 18 * s, neck, cx + 18 * s, neck + 45 * s), fill=(186, 150, 128))
    # halter dress
    top = neck + 40 * s
    d.polygon([(cx - 30 * s, top), (cx + 30 * s, top), (cx + 120 * s, h), (cx - 120 * s, h)], fill=color)
    d.polygon([(cx - 30 * s, top), (cx - 75 * s, top + 70 * s), (cx - 70 * s, top + 260 * s), (cx - 95 * s, h)], fill=(186, 150, 128))
    d.polygon([(cx + 30 * s, top), (cx + 75 * s, top + 70 * s), (cx + 70 * s, top + 260 * s), (cx + 95 * s, h)], fill=(186, 150, 128))
    d.polygon([(cx - 30 * s, top), (cx + 30 * s, top), (cx + 120 * s, h), (cx - 120 * s, h)], fill=color)
    if sequin:
        random.seed(int(cx))
        for _ in range(int(700 * s)):
            y = random.uniform(top + 20 * s, h); half = 30 * s + (y - top) / (h - top) * 90 * s
            x = random.uniform(cx - half, cx + half); r = random.uniform(1.5, 4) * s
            v = random.randint(90, 255); d.ellipse((x - r, y - r, x + r, y + r), fill=(v, v, v))
    return im
def caption(im, txt):
    d = ImageDraw.Draw(im); d.text((24, im.size[1] - 40), txt, fill=(140, 140, 140), font=font(18, False))
# hero 2-up (each 900x1200)
for i, (base, tint, col) in enumerate([((10, 10, 14), (255, 210, 150), (18, 18, 22)), ((24, 22, 20), (220, 200, 255), (30, 28, 34))], 1):
    im = figure(bokeh(900, 1200, i, base, tint), 450 if i == 1 else 430, 1.6, col)
    if i == 2: im = im.convert('L').convert('RGB')
    caption(im, 'STUDIO F DEMO · TEST IMAGE'); im.save(f'{OUT}/hero-{i}.jpg', quality=84)
# campaign banners
for name, (w, h) in {'campaign-desktop': (1920, 760), 'campaign-mobile': (900, 1200)}.items():
    im = Image.new('RGB', (w, h), (60, 52, 34)); d = ImageDraw.Draw(im)
    for y in range(h): d.line([(0, y), (w, y)], fill=(int(70 - 30 * y / h), int(60 - 28 * y / h), int(38 - 18 * y / h)))
    im = figure(im, w // 2, h / 760 * 1.05, (90, 30, 40), sequin=False)
    d = ImageDraw.Draw(im); big = font(int(h * .11)); sm = font(int(h * .035))
    if w > h:
        d.text((90, h * .30), 'black sale', fill=(240, 230, 210), font=sm); d.text((90, h * .38), 'hasta', fill=(240, 230, 210), font=sm)
        d.text((90, h * .45), '35%OFF', fill=(240, 230, 210), font=big)
        d.text((w - 620, h * .38), 'adicional', fill=(240, 230, 210), font=sm); d.text((w - 620, h * .45), 'ENVÍO GRATIS', fill=(240, 230, 210), font=font(int(h * .08)))
    else:
        d.text((60, 80), 'black sale · hasta', fill=(240, 230, 210), font=sm); d.text((60, 130), '35%OFF', fill=(240, 230, 210), font=big)
    caption(im, 'STUDIO F DEMO · TEST IMAGE'); im.save(f'{OUT}/{name}.jpg', quality=84)
# category tiles: dark background with garment silhouette
SH = {'pantalones': ([(33,14),(67,14),(70,110),(54,110),(50,45),(46,110),(30,110)], (120,120,125)),
      'blusas': ([(34,24),(44,20),(50,26),(56,20),(66,24),(80,92),(71,94),(64,48),(64,100),(36,100),(36,48),(29,94),(20,92)], (240,238,232)),
      'bolsos': ([(24,52),(76,52),(80,98),(20,98)], (190,160,120)),
      'vestidos': ([(38,18),(41,14),(44,22),(56,22),(59,14),(62,18),(63,40),(78,108),(22,108),(37,40)], (120,30,45)),
      'jeans': ([(33,14),(67,14),(70,110),(54,110),(50,45),(46,110),(30,110)], (80,110,160)),
      'zapatos': ([(18,78),(22,64),(40,60),(58,66),(76,70),(84,78),(84,86),(18,86)], (200,170,90))}
for k, (poly, col) in SH.items():
    W, H = 600, 720; im = Image.new('RGB', (W, H), (8, 8, 8)); g = Image.new('RGB', (W, H), (0, 0, 0))
    ImageDraw.Draw(g).ellipse((80, 120, 520, 600), fill=(140, 110, 60)); im = Image.blend(im, g.filter(ImageFilter.GaussianBlur(70)), .5)
    d = ImageDraw.Draw(im); d.polygon([(x * 4.2 + 90, y * 4.2 + 60) for x, y in poly], fill=col)
    caption(im, 'TEST IMAGE'); im.save(f'{OUT}/cat-{k}.jpg', quality=84)
print('ok')
