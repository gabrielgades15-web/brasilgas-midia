"""Artes da Black Friday Brasilgás a partir das bases do Canva do Gabriel (templates/black-friday/).

Troca o logo antigo do Canva pelo LOGO OFICIAL e acrescenta botão do WhatsApp, horário e endereço.
Uso: python3 black_friday.py feed|story|quadrado saida.png [--kicker "É AMANHÃ!"]
"""
import sys, base64, pathlib, argparse
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).parent
B64 = lambda p: base64.b64encode((BASE / p).read_bytes()).decode()
WA = ('<svg width="56" height="56" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 '
      '14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 '
      '2.1c.1.2.1.4 0 .6l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:%(W)dpx;height:%(H)dpx;overflow:hidden;background:#070707;font-family:'Montserrat',sans-serif;color:#fff;position:relative}
.bg{position:absolute;left:0;width:1080px}
.logo{position:absolute;background:#fff;border-radius:18px;padding:14px 22px 16px;line-height:1;box-shadow:0 8px 24px rgba(0,0,0,.35)}
.logo .w{font-weight:900;font-size:50px;letter-spacing:1px;color:#1D4FA3}.logo .w i{font-style:normal;color:#E1061A}
.logo .p{margin-top:8px;background:#E1061A;color:#fff;font-weight:800;font-size:30px;letter-spacing:3px;text-align:center;padding:6px 10px;border-radius:4px}
.selo{position:absolute;background:#1C3A8C;border-radius:40px;padding:12px 26px;font-weight:800;font-size:24px;letter-spacing:1px}
.kick{position:absolute;left:50%%;transform:translateX(-50%%) rotate(-3deg);background:#FFC72C;color:#7A0A12;font-family:'Anton';font-size:46px;
      letter-spacing:2px;padding:6px 30px;border-radius:10px;box-shadow:0 8px 20px rgba(0,0,0,.4);white-space:nowrap}
.off{position:absolute;left:0;right:0;text-align:center}
.off b{display:block;font-family:'Anton';font-size:118px;line-height:1;letter-spacing:2px;text-shadow:0 6px 0 #8a0010,0 10px 30px rgba(0,0,0,.6)}
.off span{display:inline-block;margin-top:10px;background:#E1061A;font-weight:900;font-size:30px;letter-spacing:1px;padding:8px 24px;border-radius:8px}
.cta{position:absolute;left:64px;right:64px;background:#A30F1C;border:3px solid rgba(255,255,255,.18);border-radius:28px;padding:12px 30px;display:flex;align-items:center;justify-content:center;gap:24px;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.wa{width:90px;height:90px;border-radius:50%%;background:#25D366;display:flex;align-items:center;justify-content:center;flex:none}
.cta b{display:block;font-family:'Anton';font-size:58px;letter-spacing:1px;line-height:1.05}.cta span{display:block;font-weight:800;font-size:26px;margin-top:2px}
.foot{position:absolute;left:40px;right:40px;text-align:center;font-weight:700;font-size:22px;line-height:1.45;text-shadow:0 2px 8px rgba(0,0,0,.8)}
"""

FOOT = "Segunda a sábado, das 7h às 20h · Domingos e feriados, das 7h às 13h<br>Alameda Padre Rolim, 139 · Castanhal"


def estrela(n=22, r1=50, r2=43):
    import math
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        t = math.pi * i / n
        pts.append(f"{50 + r * math.cos(t):.1f}% {50 + r * math.sin(t):.1f}%")
    return "polygon(" + ",".join(pts) + ")"


LOGO = "data:image/svg+xml;base64," + base64.b64encode((BASE / "logo/brasilgas-oficial-caixa.svg").read_bytes()).decode()
BOT = f'<img style="width:100%;display:block" src="data:image/png;base64,{B64("templates/black-friday/botijao-real.png")}">'  # foto real do botijão (asset das artes do Gabriel no Canva)


def html(fmt, kicker, cta_txt):
    """Botijão P13 em destaque (ilustração prata com lacre) + elementos das artes do Canva."""
    data = (kicker + " · " if kicker else "") + "26 E 27/11"
    if fmt == "story":
        W, H = 1080, 1920
        corpo = f"""
<img class="bg" style="top:0" src="data:image/png;base64,{B64('templates/black-friday/base-selo.png')}">
<div style="position:absolute;left:170px;right:150px;top:110px;height:160px;background:linear-gradient(90deg,#000 0%,#000 72%,#2a0203 88%,#5a0304 100%);filter:blur(10px);border-radius:30px"></div>
<div style="position:absolute;left:180px;right:158px;top:116px;height:150px;background:linear-gradient(90deg,#000 0%,#000 74%,#300203 90%,#5a0304 100%);border-radius:16px;filter:blur(2px)"></div>
<img src="{LOGO}" style="position:absolute;left:50%;top:92px;width:400px;transform:translateX(-50%);filter:drop-shadow(0 8px 20px rgba(0,0,0,.4))">
{f'<div class="kick" style="top:282px;font-size:32px;padding:3px 24px">{kicker}</div>' if kicker else ''}
<div style="position:absolute;left:0;right:0;top:729px;height:1111px;background:radial-gradient(ellipse 60% 45% at 50% 50%,#7a0a12 0%,#2a0306 55%,#000 80%)"></div>
<div style="position:absolute;left:150px;top:760px;width:640px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">{BOT}</div>
<div style="position:absolute;left:640px;top:1150px;width:400px;height:400px;background:#E1061A;clip-path:{estrela()};
     display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-8deg)">
  <b style="font-family:Anton;font-size:96px;line-height:.95;text-shadow:0 5px 0 #8a0010">R$ 10</b>
  <b style="font-family:Anton;font-size:84px;line-height:.95;color:#FFC72C;text-shadow:0 5px 0 #8a0010">OFF</b>
  <span style="font-weight:900;font-size:34px;margin-top:6px">26 e 27/11</span></div>
<div class="cta" style="top:1650px;left:110px;right:110px"><div class="wa">{WA}</div><div><b>(91) 98222-7035</b><span>{cta_txt}</span></div></div>"""
    else:
        W, H = (1080, 1350) if fmt == "feed" else (1080, 1080)
        q = fmt == "quadrado"
        y = -60 if q else 0        # no quadrado tudo sobe e o rodapé sai (vai no texto do anúncio)
        bw = 400 if q else 480
        corpo = f"""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 55% 40% at 75% 33%,#8a0b14 0%,rgba(138,11,20,0) 70%),radial-gradient(ellipse 60% 35% at 25% 30%,#4a050b 0%,rgba(0,0,0,0) 70%),#070707"></div>
<img style="position:absolute;left:{20 if not q else 40}px;top:{185+y}px;width:{570 if not q else 500}px" src="data:image/png;base64,{B64('templates/black-friday/emblema.png')}">
<div style="position:absolute;left:{585 if not q else 610}px;top:{170+y}px;width:{bw}px;filter:drop-shadow(0 26px 30px rgba(0,0,0,.7))">{BOT}</div>
<img src="{LOGO}" style="position:absolute;left:50%;top:24px;width:340px;transform:translateX(-50%);filter:drop-shadow(0 8px 20px rgba(0,0,0,.4))">
<div style="position:absolute;left:64px;right:64px;top:{(700 if q else 792)+y}px;height:{84 if q else 92}px;border-radius:26px;background:linear-gradient(90deg,#C8061A,#E1061A);
     display:flex;align-items:center;justify-content:center;font-family:Anton;font-size:{48 if q else 54}px;letter-spacing:4px;box-shadow:0 8px 20px rgba(0,0,0,.4)">{data}</div>
<div class="off" style="top:{(800 if q else 900)+y}px"><b style="{'font-size:96px' if q else ''}">R$ 10 OFF</b><span>NA RECARGA DO SEU GÁS P13</span></div>
<div class="cta" style="top:{(965 if q else 1084)+y}px;{'padding:8px 26px' if q else ''}"><div class="wa" style="{'width:72px;height:72px' if q else ''}">{WA}</div><div><b style="{'font-size:48px' if q else ''}">(91) 98222-7035</b><span>{cta_txt}</span></div></div>
{'' if q else f'<div class="foot" style="top:1262px">{FOOT}</div>'}"""
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS % dict(W=W, H=H)}</style></head>"
            f"<body>{corpo}</body></html>"), W, H


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("fmt", choices=["feed", "story", "quadrado"])
    ap.add_argument("saida")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--cta", default="Garanta no WhatsApp")
    a = ap.parse_args()
    h, W, H = html(a.fmt, a.kicker, a.cta)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(h, wait_until="networkidle")
        pg.screenshot(path=a.saida, type="png")
        b.close()
    print(a.saida)
