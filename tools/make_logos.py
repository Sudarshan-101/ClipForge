import sys, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(sys.argv[1]); name = sys.argv[2]; brand = sys.argv[3]; ink = sys.argv[4]
font_path = root / "studio/fonts/ArchivoBlack-Regular.ttf"
font = TTFont(font_path); gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm

SIZE = 104
scale = SIZE / upm
def wordmark(x0, baseline, fill):
    x = x0; out = []
    for ch in name:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        d = pen.getCommands()
        if d: out.append(f'<path d="{d}" fill="{fill}"/>')
        x += gs[g].width * scale
    return "".join(out), x

def tile(fill="#FFFFFF"):
    # rounded tile, a 9:16 frame and a play wedge: a vertical clip
    return (f'<rect width="220" height="220" rx="56" fill="{brand}"/>'
            f'<rect x="66" y="40" width="88" height="140" rx="20" fill="none" stroke="{fill}" stroke-width="14"/>'
            f'<path d="M95 80 L95 140 L132 110 Z" fill="{fill}" stroke="{fill}" stroke-width="6" stroke-linejoin="round"/>')

def svg(w, h, body): return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">{body}</svg>\n'

b = root / "web/brand"
for fname, text_fill in (("logo.svg", ink), ("logo-light.svg", "#FFFFFF")):
    wm, end = wordmark(252, 146, text_fill)
    (b / fname).write_text(svg(round(end) + 4, 220, tile() + wm))
(b / "favicon.svg").write_text(svg(220, 220, tile()))

# email logo (PNG, dark wordmark on transparent)
old = Image.open(b / "logo-email.png"); W, H = old.size
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
s = H / 220
d.rounded_rectangle([0, 0, 220 * s, 220 * s], radius=56 * s, fill=brand)
d.rounded_rectangle([66 * s, 40 * s, 154 * s, 180 * s], radius=20 * s, outline="#FFFFFF", width=round(14 * s))
d.polygon([(95 * s, 80 * s), (95 * s, 140 * s), (132 * s, 110 * s)], fill="#FFFFFF")
f = ImageFont.truetype(str(font_path), round(SIZE * s))
d.text((252 * s, 146 * s), name, font=f, fill=ink, anchor="ls")
im.save(b / "logo-email.png")
print("logos written; wordmark width", round(end))
