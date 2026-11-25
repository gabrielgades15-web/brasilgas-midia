"""Gera o logo vetorial da Brasilgás com a bandeira Paragás (ícone azul original).

Texto convertido em curvas (não depende de fonte instalada). Saídas em logo/:
  brasilgas-logo.svg          horizontal, fundo transparente (para fundo claro)
  brasilgas-logo-caixa.svg    na caixa branca arredondada (padrão das artes)
  brasilgas-logo-negativo.svg para fundo vermelho/escuro
  paragas-bandeira.svg        só a bandeira Paragás (faixa vermelha + ícone azul)
  + PNGs em alta e a foto de perfil 1080x1080.
"""
import io, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

AQUI = pathlib.Path(__file__).parent
GF = pathlib.Path("/usr/share/fonts/truetype/google-fonts/ofl")
AZUL, VERMELHO, AZUL_PG, VERM_PG = "#1D4FA3", "#E1061A", "#2B3990", "#ED1C24"


def fonte(arq, **eixos):
    f = TTFont(arq)
    return instantiateVariableFont(f, eixos) if "fvar" in f else f


MONT_BLACK = fonte(GF / "montserrat/Montserrat[wght].ttf", wght=900)
MONT_BOLD = fonte(GF / "montserrat/Montserrat[wght].ttf", wght=700)
ROBOTO_COND = fonte(GF / "roboto/Roboto[wdth,wght].ttf", wdth=88, wght=640)


def texto(font, s, size, x, y, espaco=0.0):
    """Path SVG do texto com a linha de base em y. Retorna (d, largura, altura_maiuscula)."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm
    k = size / upm; cx = 0; ds = []
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x + cx, y)))
        ds.append(pen.getCommands())
        cx += gs[g].width * k + espaco
    cap = font["OS/2"].sCapHeight * k if hasattr(font["OS/2"], "sCapHeight") else size * .7
    return " ".join(ds), cx - espaco, cap


def icone(x, y, lado, borda_branca=False):
    """Ícone Paragás: quadrado azul, octógono branco vazado, escudo vermelho com o '1' branco (desenho 100x100)."""
    s = lado / 100
    oct_ = "30,12.5 66,12.5 66,20 83,37.5 83,63 67,80 67,88 31,88 31,80 14,63 14,37.5 30,20"
    escudo = ("41,21 59,21 68,39 68,61 55,79 54.5,85 45.5,85 45,79 32,61 32,56 38,56 38,43 32,43 32,39")
    extra = f'<rect x="1.5" y="1.5" width="97" height="97" fill="none" stroke="#fff" stroke-width="3"/>' if borda_branca else ""
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">'
            f'<rect width="100" height="100" fill="{AZUL_PG}"/>{extra}'
            f'<polygon points="{oct_}" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="miter"/>'
            f'<polygon points="{escudo}" fill="{VERM_PG}"/>'
            f'<rect x="45" y="38" width="10" height="24" fill="#fff"/></g>')


def bandeira(x, y, altura, negativo=False):
    """Faixa 'PARAGÁS' + ícone azul, como a marca Paragás usa. Retorna (svg, largura)."""
    tam = altura * 0.78
    d, w, cap = texto(ROBOTO_COND, "PARAGÁS", tam, 0, 0, espaco=tam * 0.02)
    pad = altura * 0.22
    larg_faixa = w + 2 * pad
    base = y + altura / 2 + cap / 2
    partes = []
    if not negativo:
        partes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{larg_faixa:.1f}" height="{altura:.1f}" fill="{VERM_PG}"/>')
    d, _, _ = texto(ROBOTO_COND, "PARAGÁS", tam, x + pad, base, espaco=tam * 0.02)
    partes.append(f'<path d="{d}" fill="#fff"/>')
    gap = altura * (0.05 if not negativo else 0.12)
    partes.append(icone(x + larg_faixa + gap, y, altura, borda_branca=negativo))
    return "".join(partes), larg_faixa + gap + altura


def logo(negativo=False, caixa=False):
    T = 120  # corpo do "BRASILGÁS"
    d1, w1, cap = texto(MONT_BLACK, "BRASIL", T, 0, 0, espaco=2)
    d2, w2, _ = texto(MONT_BLACK, "GÁS", T, 0, 0, espaco=2)
    W = w1 + 2 + w2
    pad = 34 if caixa else 6
    topo = pad + 24          # espaço do acento do Á
    base1 = topo + cap
    c_az, c_vm = ("#fff", "#fff") if negativo else (AZUL, VERMELHO)
    d1, _, _ = texto(MONT_BLACK, "BRASIL", T, pad, base1, espaco=2)
    d2, _, _ = texto(MONT_BLACK, "GÁS", T, pad + w1 + 2, base1, espaco=2)
    # linha 2: "REVENDA AUTORIZADA" + bandeira Paragás, ocupando a largura do nome
    h2 = 58
    y2 = base1 + 22
    tmp, wb = bandeira(0, 0, h2, negativo)
    larg_txt = W - wb - 18
    tam_txt = 22
    _, wt, cap_t = texto(MONT_BOLD, "REVENDA AUTORIZADA", tam_txt, 0, 0, espaco=0)
    esp = max(0.0, (larg_txt - wt) / (len("REVENDA AUTORIZADA") - 1))
    if esp > 9:   # texto pequeno demais para o espaço: aumenta o corpo
        tam_txt = 22 * larg_txt / (wt + 17 * 6); _, wt, cap_t = texto(MONT_BOLD, "REVENDA AUTORIZADA", tam_txt, 0, 0)
        esp = (larg_txt - wt) / 17
    d3, _, _ = texto(MONT_BOLD, "REVENDA AUTORIZADA", tam_txt, pad, y2 + h2 / 2 + cap_t / 2, espaco=esp)
    band, _ = bandeira(pad + W - wb, y2, h2, negativo)
    alt = y2 + h2 + pad
    larg = W + 2 * pad
    fundo = f'<rect width="{larg:.0f}" height="{alt:.0f}" rx="26" fill="#fff"/>' if caixa else ""
    cor_txt = "#fff" if negativo else AZUL
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {larg:.0f} {alt:.0f}" width="{larg:.0f}" height="{alt:.0f}">'
            f'{fundo}<path d="{d1}" fill="{c_az}"/><path d="{d2}" fill="{c_vm}"/>'
            f'<path d="{d3}" fill="{cor_txt}"/>{band}</svg>')


def so_bandeira():
    b, w = bandeira(0, 0, 100)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} 100" width="{w:.0f}" height="100">{b}</svg>'


def perfil(svg_neg):
    import re
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_neg).groups()
    w, h = map(float, vb)
    escala = 760 / w
    interno = svg_neg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">'
            f'<rect width="1080" height="1080" fill="{VERMELHO}"/>'
            f'<g transform="translate({(1080 - w * escala) / 2:.1f},{(1080 - h * escala) / 2:.1f}) scale({escala:.4f})">{interno}</g></svg>')


def foto_perfil():
    """Foto de perfil redonda (aprovada pelo Gabriel em 25/11): fundo branco, anel vermelho + filete azul, logo horizontal no centro."""
    from PIL import Image, ImageDraw
    W = 2160
    bg = Image.new("RGBA", (W, W), (255, 255, 255, 255)); d = ImageDraw.Draw(bg)
    d.ellipse((24, 24, W - 24, W - 24), outline=(225, 6, 26, 255), width=56)
    d.ellipse((104, 104, W - 104, W - 104), outline=(29, 79, 163, 255), width=14)
    lg = Image.open(AQUI / "brasilgas-logo.png"); w = 1700
    lg = lg.resize((w, int(lg.size[1] * w / lg.size[0])), Image.LANCZOS)
    bg.alpha_composite(lg, ((W - w) // 2, (W - lg.size[1]) // 2))
    bg.resize((1080, 1080), Image.LANCZOS).convert("RGB").save(AQUI / "brasilgas-perfil.png")


def png(svg_txt, saida, largura):
    from playwright.sync_api import sync_playwright
    import re
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_txt).groups())
    alt = round(largura * h / w)
    html = f"<html><body style='margin:0;background:transparent'>{svg_txt.replace(f'width=\"{w:.0f}\" height=\"{h:.0f}\"', f'width=\"{largura}\" height=\"{alt}\"', 1)}</body></html>"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": largura, "height": alt})
        pg.set_content(html)
        pg.screenshot(path=str(saida), omit_background=True)
        b.close()


if __name__ == "__main__":
    arquivos = {
        "brasilgas-logo.svg": logo(),
        "brasilgas-logo-caixa.svg": logo(caixa=True),
        "brasilgas-logo-negativo.svg": logo(negativo=True),
        "paragas-bandeira.svg": so_bandeira(),
    }
    for nome, svg in arquivos.items():
        (AQUI / nome).write_text(svg)
    png(arquivos["brasilgas-logo.svg"], AQUI / "brasilgas-logo.png", 2000)
    png(arquivos["brasilgas-logo-caixa.svg"], AQUI / "brasilgas-logo-caixa.png", 2000)
    png(arquivos["brasilgas-logo-negativo.svg"], AQUI / "brasilgas-logo-negativo.png", 2000)
    foto_perfil()
    png(arquivos["paragas-bandeira.svg"], AQUI / "paragas-bandeira.png", 1200)
    print("ok")
