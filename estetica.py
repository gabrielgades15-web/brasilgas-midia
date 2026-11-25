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
  PRODUTO  "botijao" (padrão) ou caminho de PNG com fundo transparente

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
    "story": dict(W=1080, H=1920, tick=80, logo_y=100, logo_w=720, kick_y=286, t_y=350, t_size=230, t_w=960,
                  prod_x=80, prod_y=800, prod_w=640, selo_x=620, selo_y=1060, selo=400,
                  cta_y=1600, cta_h=150, par_y=1772, par_w=360),
    "feed": dict(W=1080, H=1350, tick=60, logo_y=74, logo_w=600, kick_y=226, t_y=284, t_size=150, t_w=960,
                 prod_x=70, prod_y=580, prod_w=420, selo_x=560, selo_y=640, selo=380,
                 cta_y=1098, cta_h=128, par_y=1238, par_w=280),
}


def estrela(n=22, r1=50, r2=43):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        t = math.pi * i / n
        pts.append(f"{50 + r * math.cos(t):.1f}% {50 + r * math.sin(t):.1f}%")
    return "polygon(" + ",".join(pts) + ")"


def html(spec, fmt, com_ticker=True):
    f = FORMATOS[fmt]
    W, H = f["W"], f["H"]
    prod = spec.get("PRODUTO", "botijao")
    prod_src = B64("templates/black-friday/botijao-real.png") if prod == "botijao" else B64(prod)
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
<img src="data:image/png;base64,{prod_src}" style="position:absolute;left:{f['prod_x']}px;top:{f['prod_y']}px;width:{f['prod_w']}px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.7))">
{selo_html}
<div class="cta"><div class="wa">{WA}</div><div><b>(91) 98222 7035</b><span>{spec.get('CTA_SUB','peça no WhatsApp')}</span></div></div>
<img src="{PARAGAS}" style="position:absolute;left:50%;top:{f['par_y']}px;width:{f['par_w']}px;transform:translateX(-50%)">
<script>
document.querySelectorAll('[data-fit]').forEach(el=>{{let s={t_size};el.style.fontSize=s+'px';
  while(el.scrollWidth>{f['t_w']}&&s>40){{s-=4;el.style.fontSize=s+'px';}}}});
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


def video(spec, fmt, saida):
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
    filtros = (f"[0:v]scale={W*2}:{H*2},zoompan=z='1+0.00025*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s={W}x{H}:fps=30[bg];"
               f"[bg][1:v]overlay=x='-mod(t*{v}\\,{u})':y={ys[0]}[a];"
               f"[a][1:v]overlay=x='-{u}+mod(t*{v}\\,{u})':y={ys[1]}[b];"
               f"[b][1:v]overlay=x='-mod(t*{v}\\,{u})':y={ys[2]}[c];"
               f"[c][1:v]overlay=x='-{u}+mod(t*{v}\\,{u})':y={ys[3]},format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(tmp / "base.png"), "-loop", "1", "-i", str(tmp / "t.png"),
                    "-filter_complex", filtros, "-map", "[v]", "-t", "5", "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-movflags", "+faststart", str(saida)], check=True)
    capa = pathlib.Path(str(saida).rsplit(".", 1)[0] + "-capa.png")
    shot(html(spec, fmt), W, H, capa)
    return capa


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("saida"); ap.add_argument("fmt", choices=list(FORMATOS))
    ap.add_argument("--video", action="store_true")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    if a.video:
        print(a.saida, video(spec, a.fmt, a.saida))
    else:
        f = FORMATOS[a.fmt]
        shot(html(spec, a.fmt), f["W"], f["H"], a.saida)
        print(a.saida)
