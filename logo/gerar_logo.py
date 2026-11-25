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
ARCHIVO_BLACK = fonte(GF / "archivoblack/ArchivoBlack-Regular.ttf")
ROBOTO_LARGA = fonte(GF / "roboto/Roboto[wdth,wght].ttf", wdth=100, wght=560)
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


def bandeira(x, y, altura, negativo=False, font=None):
    """Faixa 'PARAGÁS' + ícone azul, como a marca Paragás usa. Retorna (svg, largura)."""
    font = font or ROBOTO_COND
    tam = altura * 0.78
    d, w, cap = texto(font, "PARAGÁS", tam, 0, 0, espaco=tam * 0.02)
    pad = altura * 0.22
    larg_faixa = w + 2 * pad
    base = y + altura / 2 + cap / 2
    partes = []
    if not negativo:
        partes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{larg_faixa:.1f}" height="{altura:.1f}" fill="{VERM_PG}"/>')
    d, _, _ = texto(font, "PARAGÁS", tam, x + pad, base, espaco=tam * 0.02)
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


# ---------- Logo da placa da loja (o original da Brasilgás, pedido do Gabriel em 25/11 às 18h) ----------
AZUL_PLACA, CINZA_PLACA, VERM_PLACA = "#1F5BD0", "#8F8F8F", "#E30613"


def botijao_pict(x, y, w):
    """Pictograma do botijão da placa (prata chapado com faixa azul), desenho 100x112."""
    s = w / 100
    prata = "url(#prata)"
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">'
            f'<rect x="30" y="0" width="40" height="22" rx="2" fill="{prata}"/>'
            f'<rect x="38" y="7" width="24" height="5" rx="2.5" fill="{AZUL_PLACA}"/><rect x="48" y="10" width="4" height="12" fill="{AZUL_PLACA}"/>'
            f'<path d="M5 44 Q5 26 23 26 H77 Q95 26 95 44 V88 Q95 104 79 104 H21 Q5 104 5 88 Z" fill="{prata}"/>'
            f'<rect x="5" y="61" width="90" height="4" fill="{AZUL_PLACA}"/>'
            f'<rect x="28" y="106" width="44" height="6" fill="{prata}"/></g>')


def quadro_icone(x, y, w):
    """Quadro azul da placa: botijão + bandeira Paragás, com borda branca. Altura = 1.04*w."""
    h = w * 1.04
    b = w * 0.035
    pict_w = w * 0.54
    band_h = w * 0.15
    band, band_w = bandeira(0, 0, band_h)
    esc = (w - 2 * b - w * 0.12) / band_w
    band_h2 = band_h * esc
    by = y + h - b - w * 0.05 - band_h2
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#fff"/>'
            f'<rect x="{x + b:.1f}" y="{y + b:.1f}" width="{w - 2 * b:.1f}" height="{h - 2 * b:.1f}" fill="{AZUL_PLACA}"/>'
            + botijao_pict(x + (w - pict_w) / 2, y + b + w * 0.06, pict_w)
            + f'<rect x="{x + w * 0.06 + b - 3:.1f}" y="{by - 3:.1f}" width="{band_w * esc + 6:.1f}" height="{band_h2 + 6:.1f}" fill="#fff"/>'
            + f'<g transform="translate({x + w * 0.06 + b:.1f},{by:.1f}) scale({esc:.4f})">{band}</g>')


DEFS = ('<defs><linearGradient id="prata" x1="0" x2="1"><stop offset="0" stop-color="#b9b3b3"/>'
        '<stop offset=".45" stop-color="#e2dddd"/><stop offset="1" stop-color="#a9a3a3"/></linearGradient></defs>')


def wordmark(x, base, T, contorno=True):
    d1, w1, cap = texto(MONT_BLACK, "BRASIL", T, x, base, espaco=T * 0.01)
    d2, w2, _ = texto(MONT_BLACK, "GÁS", T, x + w1 + T * 0.01, base, espaco=T * 0.01)
    st = f' stroke="#fff" stroke-width="{T * 0.07:.1f}" stroke-linejoin="round" paint-order="stroke"' if contorno else ""
    return (f'<path d="{d1}" fill="{AZUL_PLACA}"{st}/><path d="{d2}" fill="{CINZA_PLACA}"{st}/>'), w1 + T * 0.01 + w2, cap


def logo_placa():
    """Faixa vermelha com moldura branca, BRASILGÁS (azul + cinza) e o quadro do botijão com a bandeira Paragás."""
    T = 128
    _, ww, cap = wordmark(0, 0, T)
    H = 240                     # altura da faixa vermelha
    qw = 250                    # quadro do botijão (passa um pouco da faixa)
    padx = 46
    W = padx + ww + 50 + qw + 20
    top = (1.04 * qw - H) / 2 + 6
    base = top + H / 2 + cap / 2 + 4
    wm, _, _ = wordmark(padx, base, T)
    m = 12
    alt = 1.04 * qw + 12
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {alt:.0f}" width="{W:.0f}" height="{alt:.0f}">{DEFS}'
            f'<rect x="0" y="{top:.1f}" width="{W - qw / 2:.1f}" height="{H}" rx="14" fill="{VERM_PLACA}"/>'
            f'<rect x="{m}" y="{top + m:.1f}" width="{W - qw / 2 - 2 * m:.1f}" height="{H - 2 * m}" rx="6" fill="none" stroke="#fff" stroke-width="7"/>'
            f'{wm}{quadro_icone(W - qw - 14, 6, qw)}</svg>')


def foto_perfil_placa():
    """Foto de perfil redonda a partir da placa: fundo vermelho, moldura branca, quadro do botijão em cima e BRASILGÁS embaixo."""
    _, ww0, _ = wordmark(0, 0, 100)
    T = 100 * 800 / ww0          # nome com 800 px de largura, dentro do círculo
    wm, ww, cap = wordmark(0, 0, T)
    W = 1080
    qw = 420
    x0 = (W - ww) / 2
    wm, _, _ = wordmark(x0, 665 + 60 + cap, T)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">{DEFS}'
            f'<rect width="{W}" height="{W}" fill="{VERM_PLACA}"/>'
            f'<circle cx="540" cy="540" r="508" fill="none" stroke="#fff" stroke-width="16"/>'
            f'{quadro_icone((W - qw) / 2, 215, qw)}{wm}'
            f'</svg>')


# ---------- Logo definido pelo dono (25/11, 18h44): BRASIL azul-marinho + GÁS vermelho, bandeira Paragás embaixo ----------
AZUL_DONO, VERM_DONO = "#33348F", "#ED1C24"


def nome_dono(x, base, T):
    d1, w1, cap = texto(ARCHIVO_BLACK, "BRASIL", T, x, base, espaco=T * 0.02)
    d2, w2, _ = texto(ARCHIVO_BLACK, "GÁS", T, x + w1 + T * 0.02, base, espaco=T * 0.02)
    return f'<path d="{d1}" fill="{AZUL_DONO}"/><path d="{d2}" fill="{VERM_DONO}"/>', w1 + T * 0.02 + w2, cap


def logo_dono(largura_nome=1000, fundo=True, pad=60, rx=0):
    """BRASILGÁS em cima, bandeira Paragás centralizada embaixo (67% da largura do nome), fundo branco."""
    _, w0, _ = nome_dono(0, 0, 100)
    T = 100 * largura_nome / w0
    _, wn, cap = nome_dono(0, 0, T)
    topo = pad + T * 0.22
    base = topo + cap
    nm, _, _ = nome_dono(pad, base, T)
    _, bw0 = bandeira(0, 0, 100, font=ROBOTO_LARGA)
    bh = 100 * (wn * 0.67) / bw0
    band, bw = bandeira(pad + (wn - wn * 0.67) / 2, base + T * 0.30, bh, font=ROBOTO_LARGA)
    W = wn + 2 * pad
    H = base + T * 0.30 + bh + pad
    bg = f'<rect width="{W:.0f}" height="{H:.0f}" rx="{rx}" fill="#fff"/>' if fundo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">{bg}{nm}{band}</svg>')


def perfil_dono():
    """Foto de perfil redonda: fundo branco, BRASILGÁS e a bandeira Paragás embaixo, centralizados no círculo."""
    import re
    svg = logo_dono(largura_nome=1000, fundo=False, pad=0)
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    esc = 860 / w
    interno = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">'
            f'<rect width="1080" height="1080" fill="#fff"/>'
            f'<g transform="translate({(1080 - w * esc) / 2:.1f},{(1080 - h * esc) / 2:.1f}) scale({esc:.4f})">{interno}</g></svg>')


# ---------- Logo do Instagram (25/11, 20h34 — modelo de vídeo do Gabriel) ----------
def logo_instagram():
    """Caixa branca: BRASIL azul + GÁS cinza (fonte grossa) e o quadro azul do botijão com a bandeira Paragás à direita."""
    T = 150
    d1, w1, cap = texto(ARCHIVO_BLACK, "BRASIL", T, 0, 0, espaco=T * 0.01)
    d2, w2, _ = texto(ARCHIVO_BLACK, "GÁS", T, 0, 0, espaco=T * 0.01)
    padx, H = 52, 250
    qw = 214
    base = H / 2 + cap / 2 + 6
    d1, _, _ = texto(ARCHIVO_BLACK, "BRASIL", T, padx, base, espaco=T * 0.01)
    d2, _, _ = texto(ARCHIVO_BLACK, "GÁS", T, padx + w1 + T * 0.01, base, espaco=T * 0.01)
    W = padx + w1 + T * 0.01 + w2 + 34 + qw + 16
    qx, qy = W - qw - 16, (H - qw * 1.04) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H}" width="{W:.0f}" height="{H}">{DEFS}'
            f'<rect width="{W:.0f}" height="{H}" fill="#fff"/>'
            f'<path d="{d1}" fill="#1E3A9C"/><path d="{d2}" fill="#5A5A5A"/>{quadro_icone(qx, qy, qw)}</svg>')


if __name__ == "__main__":
    arquivos = {
        "brasilgas-logo.svg": logo(),
        "brasilgas-logo-caixa.svg": logo(caixa=True),
        "brasilgas-logo-negativo.svg": logo(negativo=True),
        "paragas-bandeira.svg": so_bandeira(),
    }
    arquivos["brasilgas-placa.svg"] = logo_placa()
    arquivos["brasilgas-instagram.svg"] = logo_instagram()
    arquivos["brasilgas-oficial.svg"] = logo_dono()
    arquivos["brasilgas-oficial-caixa.svg"] = logo_dono(pad=64, rx=36)   # usado no topo das artes
    arquivos["brasilgas-perfil-oficial.svg"] = perfil_dono()
    arquivos["brasilgas-perfil-placa.svg"] = foto_perfil_placa()
    for nome, svg in arquivos.items():
        (AQUI / nome).write_text(svg)
    png(arquivos["brasilgas-logo.svg"], AQUI / "brasilgas-logo.png", 2000)
    png(arquivos["brasilgas-logo-caixa.svg"], AQUI / "brasilgas-logo-caixa.png", 2000)
    png(arquivos["brasilgas-logo-negativo.svg"], AQUI / "brasilgas-logo-negativo.png", 2000)
    foto_perfil()
    png(arquivos["paragas-bandeira.svg"], AQUI / "paragas-bandeira.png", 1200)
    png(arquivos["brasilgas-placa.svg"], AQUI / "brasilgas-placa.png", 2000)
    png(arquivos["brasilgas-perfil-placa.svg"], AQUI / "brasilgas-perfil-placa.png", 1080)
    png(arquivos["brasilgas-oficial.svg"], AQUI / "brasilgas-oficial.png", 2000)
    png(arquivos["brasilgas-perfil-oficial.svg"], AQUI / "brasilgas-perfil-oficial.png", 1080)
    png(arquivos["brasilgas-instagram.svg"], AQUI / "brasilgas-instagram.png", 2000)
    print("ok")
