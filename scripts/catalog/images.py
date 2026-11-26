import os, sys, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import data
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
W, H = 1000, 1250; S = 10  # 100x125 units
def slug(s): return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).strip('-')
def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def shade(rgb, f): return tuple(max(0, min(255, int(v * f))) for v in rgb)
def P(pts): return [(x * S, y * S) for x, y in pts]
SH = {
 'dress': [[(38,18),(41,14),(44,22),(56,22),(59,14),(62,18),(63,40),(78,108),(22,108),(37,40)]],
 'top': [[(35,25),(45,22),(50,26),(55,22),(65,25),(80,38),(72,46),(66,40),(66,90),(34,90),(34,40),(28,46),(20,38)]],
 'shirt': [[(34,24),(44,20),(50,26),(56,20),(66,24),(80,92),(71,94),(64,48),(64,100),(36,100),(36,48),(29,94),(20,92)]],
 'jacket': [[(33,24),(44,20),(50,30),(56,20),(67,24),(80,90),(71,92),(65,50),(65,95),(35,95),(35,50),(29,92),(20,90)]],
 'pants': [[(33,14),(67,14),(70,110),(54,110),(50,45),(46,110),(30,110)]],
 'skirt': [[(36,24),(64,24),(78,100),(22,100)]],
 'shoe': [[(18,78),(22,64),(40,60),(58,66),(76,70),(84,78),(84,86),(18,86)]],
 'bag': [[(24,52),(76,52),(80,98),(20,98)]],
}
def draw(shape, color, alt, out):
    bg = (238, 234, 228) if not alt else (226, 222, 216)
    im = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(im)
    # floor gradient
    for y in range(H):
        f = 1 - 0.06 * (y / H); d.line([(0, y), (W, y)], fill=shade(bg, f))
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse((200, 1060, 800, 1140), fill=110)
    im.paste((90, 85, 80), mask=sh.filter(ImageFilter.GaussianBlur(30)))
    rgb = hx(color); d = ImageDraw.Draw(im)
    if alt:  # detail crop look: scale shape up
        z = Image.new('RGBA', (W, H)); dd = ImageDraw.Draw(z)
    if shape == 'earring':
        for cx in (38, 62):
            d.ellipse(P([(cx-14, 45), (cx+14, 85)]), outline=rgb, width=70)
            d.ellipse(P([(cx-12, 47), (cx+2, 62)]), outline=shade(rgb, 1.35), width=12)
    else:
        for poly in SH[shape]:
            d.polygon(P(poly), fill=rgb)
            # light from left: highlight stripe
            hl = Image.new('L', (W, H), 0); ImageDraw.Draw(hl).polygon(P(poly), fill=255)
            grad = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(grad)
            for x in range(W): gd.line([(x, 0), (x, H)], fill=int(60 * abs((x - W * .42) / W)))
            dark = Image.new('RGB', (W, H), (0, 0, 0))
            m = Image.composite(grad, Image.new('L', (W, H), 0), hl)
            im.paste(dark, mask=m)
        if shape == 'bag':
            d.arc(P([(32, 22), (68, 80)]), 180, 360, fill=(201, 162, 74), width=22)
        if shape in ('shirt', 'jacket'):
            d.line(P([(50, 30), (50, 98)]), fill=shade(rgb, .7), width=8)
        if shape == 'skirt':
            for x in range(30, 72, 6): d.line(P([(x + (x-50)*-.3, 26), (x + (x-50)*.25, 99)]), fill=shade(rgb, .82), width=5)
        if shape == 'shoe':
            d.polygon(P([(18, 86), (84, 86), (84, 92), (18, 92)]), fill=(245, 245, 245) if sum(rgb) < 500 else (30, 30, 30))
    if alt:
        im = im.crop((150, 150, 850, 1025)).resize((W, H))
    try: f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 30)
    except Exception: f = ImageFont.load_default()
    ImageDraw.Draw(im).text((40, H - 60), 'STUDIO F DEMO · TEST IMAGE', fill=(150, 145, 138), font=f)
    im.save(out, 'JPEG', quality=86)
n = 0
for p in data.PRODUCTS:
    for c in p[5]:
        for alt in (0, 1):
            draw(p[8], data.COLORS[c], alt, os.path.join(OUT, f'{slug(p[0])}-{slug(c)}-{alt+1}.jpg')); n += 1
print(n, 'images')
