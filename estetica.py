"""Estética nova da Brasilgás (25/11/2026, a partir do vídeo-modelo do Gabriel).

Fundo preto com fumaça vermelha, faixas de texto correndo no topo e na base, logo do Instagram
(BRASIL azul + GÁS cinza + quadro do botijão Paragás) em caixa branca, faixa amarela, título grande
em duas cores (vermelho + branco), botijão real, selo em estrela opcional, botão vermelho do WhatsApp
e a bandeira Paragás embaixo.

Spec (JSON):
  KICKER   faixa amarela (curta)                 ex.: "Entrega em Castanhal"
  L1       linha 1 do título, em vermelho        ex.: "Acabou"
  L2       linha 2 do título, em branco          ex.: "o gás?"
  SELO     lista de 1 a 3 linhas do selo (opcional) ex.: ["Gás do", "Povo", "aqui"]
  CTA_SUB  frase do botão                        ex.: "peça sua recarga"
  TICKER   texto das faixas                      ex.: "GÁS P13 PARAGÁS > BRASILGAS"
  PRODUTO  "botijao" (padrão), "nenhum" ou caminho de PNG com fundo transparente
  FOTO     foto real (fotos/<arquivo>.jpg), tratada com tratar_foto.py e mostrada num quadro com borda branca
           abaixo do título (com FOTO, o padrão do PRODUTO vira "nenhum")
  FOTO_POS enquadramento da foto no quadro (CSS object-position)  ex.: "50% 40%"
  INFO     lista de 1 a 3 linhas curtas em branco abaixo da foto (destaques: endereço, horário)
  CARTOES  lista de [rótulo, valor] em quadros grandes no lugar do produto (ex.: horário)
  T_SIZE   tamanho máximo do título (padrão 200 no story, 130 no feed)

Uso:
  python3 estetica.py spec.json saida.png story|feed
  python3 estetica.py spec.json saida.mp4 story|feed --video   (5 s: faixas correndo + zoom leve; gera também a capa .png)
"""
import sys, json, base64, pathlib, argparse, subprocess, tempfile, math
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).parent
B64 = lambda p: base64.b64encode((BASE / p).read_bytes()).decode()
LOGO = "data:image/svg+xml;base64," + B64("logo/brasilgas-instagram.svg")
PARAGAS = "data:image/svg+xml;base64," + B64("logo/paragas-bandeira.svg")
WA = ('<svg viewBox="0 0 24 24" fill="#fff" width="100%" height="100%"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 '
      '14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 '
      '2.1c.1.2.1.4 0 .6l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>')

FORMATOS = {
    # y de cada bloco
    "story": dict(W=1080, H=1920, tick=80, logo_y=100, logo_w=460, kick_y=0, t_y=0, t_size=200, t_w=960,
                  prod_x=90, prod_y=0, prod_w=600, selo_x=620, selo_y=0, selo=390,
                  cta_y=1640, cta_h=150, par_y=0, par_w=0),
    "feed": dict(W=1080, H=1350, tick=60, logo_y=72, logo_w=330, kick_y=0, t_y=0, t_size=130, t_w=960,
                 prod_x=90, prod_y=0, prod_w=390, selo_x=560, selo_y=0, selo=360,
                 cta_y=1146, cta_h=128, par_y=0, par_w=0),
}


def estrela(n=22, r1=50, r2=43):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        t = math.pi * i / n
        pts.append(f"{50 + r * math.cos(t):.1f}% {50 + r * math.sin(t):.1f}%")
    return "polygon(" + ",".join(pts) + ")"


def _proporcao_logo():
    import re
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', (BASE / "logo/brasilgas-instagram.svg").read_text()).groups())
    return h / w


def html(spec, fmt, com_ticker=True):
    f = dict(FORMATOS[fmt])
    lh = f["logo_w"] * _proporcao_logo()
    story = fmt == "story"
    f["kick_y"] = f["logo_y"] + lh + (24 if story else 18)
    f["t_y"] = f["kick_y"] + (72 if story else 58)
    f["prod_y"] = f["t_y"] + f["t_size"] * 1.8 + (40 if story else 24)
    if spec.get("T_SIZE"):
        f["t_size"] = spec["T_SIZE"]
        f["prod_y"] = f["t_y"] + f["t_size"] * 1.8 + (40 if story else 24)
    f["selo_y"] = f["prod_y"] + (260 if story else 90)
    W, H = f["W"], f["H"]
    prod = spec.get("PRODUTO", "nenhum" if (spec.get("FOTO") or spec.get("CARTOES")) else "botijao")
    prod_src = "" if prod == "nenhum" else (B64("templates/black-friday/botijao-real.png") if prod == "botijao" else B64(prod))
    foto_html = ""
    if spec.get("FOTO"):
        from tratar_foto import tratar
        tf = tratar(BASE / spec["FOTO"])
        info = spec.get("INFO") or []
        info_h = (len(info) * (58 if story else 44) + 30) if info else 0
        fy = f["prod_y"]
        fh = f["cta_y"] - fy - info_h - (40 if story else 26)
        foto_html = (f'<div style="position:absolute;left:70px;right:70px;top:{fy:.0f}px;height:{fh:.0f}px;border:8px solid #fff;border-radius:34px;'
                     f'overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.7)"><img src="data:image/jpeg;base64,{base64.b64encode(tf.read_bytes()).decode()}" '
                     f'style="width:100%;height:100%;object-fit:cover;object-position:{spec.get("FOTO_POS","50% 50%")}"></div>')
        if info:
            foto_html += (f'<div style="position:absolute;left:50px;right:50px;top:{fy + fh + (22 if story else 14):.0f}px;text-align:center;'
                          f'font-weight:800;font-size:{46 if story else 34}px;line-height:1.22;text-shadow:0 4px 14px rgba(0,0,0,.8)">'
                          + "<br>".join(info) + '</div>')
        f["selo_y"] = fy + fh - f["selo"] * .75
        f["selo_x"] = W - f["selo"] - 20
    elif spec.get("CARTOES"):
        # quadro de informação grande (ex.: horário): linhas [rótulo, valor]
        cards = spec["CARTOES"]
        fy = f["prod_y"] + 10
        livre = f["cta_y"] - fy - (50 if story else 30)
        gap = 30 if story else 18
        ch = (livre - gap * (len(cards) - 1)) / len(cards)
        for i, (rot, val) in enumerate(cards):
            y = fy + i * (ch + gap)
            foto_html += (f'<div style="position:absolute;left:70px;right:70px;top:{y:.0f}px;height:{ch:.0f}px;border-radius:30px;'
                          f'background:linear-gradient(180deg,rgba(40,0,4,.9),rgba(15,0,2,.9));border:4px solid #E30B13;'
                          f'box-shadow:0 16px 40px rgba(0,0,0,.6);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
                          f'<div style="background:#FFD23F;color:#D90812;font-weight:900;font-size:{40 if story else 30}px;padding:6px 26px;border-radius:12px;'
                          f'text-transform:uppercase;letter-spacing:1px">{rot}</div>'
                          f'<div data-fit2 style="font-family:Anton;font-size:{150 if story else 100}px;line-height:1.05;margin-top:14px;white-space:nowrap">{val}</div></div>')
    elif spec.get("INFO"):
        info = spec["INFO"]
        lh_ = 58 if story else 44
        iy = f["cta_y"] - len(info) * lh_ - (40 if story else 26)
        foto_html = (f'<div style="position:absolute;left:50px;right:50px;top:{iy:.0f}px;text-align:center;font-weight:800;'
                     f'font-size:{46 if story else 34}px;line-height:1.22;text-shadow:0 4px 14px rgba(0,0,0,.8)">' + "<br>".join(info) + '</div>')
        # o produto e o selo cabem acima do texto
        alto = iy - f["prod_y"] - 20
        f["prod_w"] = min(f["prod_w"], int(alto * 975 / 1200))
        f["selo_y"] = f["prod_y"] + alto * .25
    tick = (spec.get("TICKER") or "GÁS P13 PARAGÁS > BRASILGAS > ENTREGA EM CASTANHAL").upper()
    tick_txt = (" > ".join([tick] * 6))
    selo = spec.get("SELO") or []
    selo_html = ""
    if selo:
        linhas = "".join(
            f'<b style="font-family:Anton;font-size:{s}px;line-height:.95;color:{c};text-shadow:0 5px 0 #8a0010">{t}</b>'
            for t, s, c in zip(selo, [92, 84, 40] if len(selo) == 3 else [96, 84], ["#fff", "#FFC72C", "#fff"]))
        selo_html = (f'<div style="position:absolute;left:{f["selo_x"]}px;top:{f["selo_y"]}px;width:{f["selo"]}px;height:{f["selo"]}px;'
                     f'background:#D90812;clip-path:{estrela()};display:flex;flex-direction:column;align-items:center;justify-content:center;'
                     f'text-align:center;transform:rotate(-8deg)">{linhas}</div>')
    tk = (f'<div class="tk" style="top:6px">{tick_txt}</div><div class="tk r" style="top:{f["tick"]//2+4}px">{tick_txt}</div>'
          f'<div class="tk" style="top:{H - f["tick"] + 2}px">{tick_txt}</div><div class="tk r" style="top:{H - f["tick"]//2}px">{tick_txt}</div>'
          if com_ticker else "")
    t_size = f["t_size"]
    prod_img = (f'<img src="data:image/png;base64,{prod_src}" style="position:absolute;left:{f["prod_x"]}px;top:{f["prod_y"]}px;'
                f'width:{f["prod_w"]}px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.7))">') if prod_src else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;font-family:Montserrat,sans-serif;color:#fff;
  background:radial-gradient(ellipse 45% 30% at 88% 12%,rgba(150,8,16,.75),transparent 70%),
             radial-gradient(ellipse 55% 35% at 8% 72%,rgba(140,6,14,.7),transparent 72%),
             radial-gradient(ellipse 40% 25% at 95% 88%,rgba(120,5,12,.55),transparent 70%),#050505}}
.tk{{position:absolute;left:-40px;white-space:nowrap;color:#E0141C;font-weight:500;font-size:{30 if fmt=='story' else 24}px;letter-spacing:.5px;opacity:.95}}
.tk.r{{left:-420px}}
.kick{{position:absolute;left:50%;top:{f['kick_y']}px;transform:translateX(-50%) rotate(-2deg);background:#FFD23F;color:#D90812;
  font-weight:900;font-size:{40 if fmt=='story' else 32}px;letter-spacing:1px;padding:8px 34px;border-radius:14px;white-space:nowrap;
  box-shadow:0 8px 20px rgba(0,0,0,.45);text-transform:uppercase}}
.tit{{position:absolute;left:0;right:0;top:{f['t_y']}px;display:flex;flex-direction:column;align-items:center;text-align:center;font-family:'Archivo Black';text-transform:uppercase;line-height:.9;letter-spacing:-2px}}
.tit div{{display:inline-block;white-space:nowrap}}
.l1{{color:#E8141C;text-shadow:0 8px 24px rgba(0,0,0,.6)}}
.l2{{color:#fff;text-shadow:0 10px 0 rgba(0,0,0,.35),0 14px 30px rgba(0,0,0,.6)}}
.cta{{position:absolute;left:70px;right:70px;top:{f['cta_y']}px;height:{f['cta_h']}px;background:#E30B13;border-radius:{f['cta_h']//3}px;
  display:flex;align-items:center;justify-content:center;gap:26px;box-shadow:0 12px 30px rgba(0,0,0,.5)}}
.cta .wa{{width:{f['cta_h']*0.5:.0f}px;height:{f['cta_h']*0.5:.0f}px;background:#25D366;border-radius:50%;padding:{f['cta_h']*0.08:.0f}px;flex:none}}
.cta b{{display:block;font-family:Anton;font-size:{f['cta_h']*0.46:.0f}px;letter-spacing:4px;line-height:1}}
.cta span{{display:block;font-family:Anton;font-size:{f['cta_h']*0.2:.0f}px;letter-spacing:1px;text-align:center;margin-top:4px}}
</style></head><body>
{tk}
<img src="{LOGO}" style="position:absolute;left:50%;top:{f['logo_y']}px;width:{f['logo_w']}px;transform:translateX(-50%);box-shadow:0 10px 30px rgba(0,0,0,.5)">
{f'<div class="kick">{spec["KICKER"]}</div>' if spec.get("KICKER") else ''}
<div class="tit"><div class="l1" data-fit>{spec.get('L1','')}</div><div class="l2" data-fit>{spec.get('L2','')}</div></div>
{foto_html}
{prod_img}
{selo_html}
<div class="cta"><div class="wa">{WA}</div><div><b>(91) 98222 7035</b><span>{spec.get('CTA_SUB','peça no WhatsApp')}</span></div></div>
{f'<img src="{PARAGAS}" style="position:absolute;left:50%;top:{f["par_y"]}px;width:{f["par_w"]}px;transform:translateX(-50%)">' if f["par_w"] else ''}
<script>
document.querySelectorAll('[data-fit]').forEach(el=>{{let s={t_size};el.style.fontSize=s+'px';
  while(el.scrollWidth>{f['t_w']}&&s>40){{s-=4;el.style.fontSize=s+'px';}}}});
document.querySelectorAll('[data-fit2]').forEach(el=>{{let s=parseFloat(el.style.fontSize);
  while(el.scrollWidth>{W-200}&&s>30){{s-=4;el.style.fontSize=s+'px';}}}});
</script></body></html>"""


def shot(h, W, H, saida):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(h, wait_until="networkidle")
        pg.wait_for_timeout(150)
        pg.screenshot(path=str(saida))
        b.close()


def faixa(texto, alto, tam, saida):
    """Faixa de texto que se repete (para correr no vídeo). Retorna a largura de 1 repetição."""
    from PIL import Image, ImageDraw, ImageFont
    fonte = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf", tam)
    try:
        fonte.set_variation_by_axes([500])
    except Exception:
        pass
    unidade = texto.upper() + " > "
    u = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(unidade, font=fonte))
    n = math.ceil(1080 / u) + 2
    im = Image.new("RGBA", (u * n, alto), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 2), unidade * n, font=fonte, fill=(224, 20, 28, 242))
    im.save(saida)
    return u


def video(spec, fmt, saida, dur=5):
    f = FORMATOS[fmt]
    W, H = f["W"], f["H"]
    tmp = pathlib.Path(tempfile.mkdtemp())
    shot(html(spec, fmt, com_ticker=False), W, H, tmp / "base.png")
    tick = (spec.get("TICKER") or "GÁS P13 PARAGÁS > BRASILGAS > ENTREGA EM CASTANHAL")
    tam = 30 if fmt == "story" else 24
    hl = f["tick"] // 2
    u = faixa(tick, hl, tam, tmp / "t.png")
    v = 90  # px por segundo
    ys = [6, hl + 4, H - f["tick"] + 2, H - hl]
    filtros = (f"[0:v]scale={W*2}:{H*2},zoompan=z='1+0.00025*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={dur*30}:s={W}x{H}:fps=30[bg];"
               f"[bg][1:v]overlay=x='-mod(t*{v}\\,{u})':y={ys[0]}[a];"
               f"[a][1:v]overlay=x='-{u}+mod(t*{v}\\,{u})':y={ys[1]}[b];"
               f"[b][1:v]overlay=x='-mod(t*{v}\\,{u})':y={ys[2]}[c];"
               f"[c][1:v]overlay=x='-{u}+mod(t*{v}\\,{u})':y={ys[3]},format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(tmp / "base.png"), "-loop", "1", "-i", str(tmp / "t.png"),
                    "-filter_complex", filtros, "-map", "[v]", "-t", str(dur), "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-movflags", "+faststart", str(saida)], check=True)
    capa = pathlib.Path(str(saida).rsplit(".", 1)[0] + "-capa.png")
    shot(html(spec, fmt), W, H, capa)
    return capa


def reel(specs, saida, dur=4, trans=0.5):
    """Reel vertical com várias cenas (uma por spec), transição suave entre elas. Gera também a capa (1ª cena)."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    clipes = []
    for i, sp in enumerate(specs):
        c = tmp / f"c{i}.mp4"
        video(sp, "story", c, dur=dur)
        clipes.append(c)
    entradas, filtros, ant, off = [], [], "[0:v]", 0.0
    for c in clipes:
        entradas += ["-i", str(c)]
    for i in range(1, len(clipes)):
        off += dur - trans
        saida_lbl = f"[x{i}]"
        filtros.append(f"{ant}[{i}:v]xfade=transition=fade:duration={trans}:offset={off:.2f}{saida_lbl}")
        ant = saida_lbl
    subprocess.run(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros) + f";{ant}format=yuv420p[v]",
                    "-map", "[v]", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart",
                    str(saida)], check=True)
    capa = pathlib.Path(str(saida).rsplit(".", 1)[0] + "-capa.png")
    shot(html(specs[0], "story"), 1080, 1920, capa)
    return capa


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("saida"); ap.add_argument("fmt", choices=list(FORMATOS))
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--reel", action="store_true", help="spec é uma LISTA de cenas")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    if a.reel:
        print(a.saida, reel(spec, a.saida))
    elif a.video:
        print(a.saida, video(spec, a.fmt, a.saida))
    else:
        f = FORMATOS[a.fmt]
        shot(html(spec, a.fmt), f["W"], f["H"], a.saida)
        print(a.saida)
