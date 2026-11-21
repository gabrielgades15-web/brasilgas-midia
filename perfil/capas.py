"""Capas dos destaques do Instagram (1080x1920; o Instagram mostra o círculo central)."""
import pathlib
from playwright.sync_api import sync_playwright
ICONES = {
 "gas-do-povo": ("GÁS DO POVO", '<path d="M50 8c4 18 22 26 22 48a22 22 0 0 1-44 0c0-10 5-17 10-22 1 8 5 12 9 13-3-14 1-28 3-39z" fill="#fff"/><path d="M50 52c3 7 10 9 10 17a10 10 0 0 1-20 0c0-6 4-10 10-17z" fill="#FFC72C"/>'),
 "entrega": ("ENTREGA", '<circle cx="24" cy="72" r="11" fill="none" stroke="#fff" stroke-width="7"/><circle cx="78" cy="72" r="11" fill="none" stroke="#fff" stroke-width="7"/><path d="M24 72h22l10-26h14l8 26M46 46H30M56 46l-6-12h-8" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><rect x="62" y="28" width="16" height="20" rx="4" fill="#FFC72C"/>'),
 "agua-20l": ("ÁGUA 20L", '<rect x="40" y="10" width="20" height="10" rx="3" fill="#FFC72C"/><path d="M38 22h24l6 12H32z" fill="#fff"/><rect x="26" y="34" width="48" height="56" rx="12" fill="#fff"/><path d="M50 50c5 8 9 11 9 17a9 9 0 0 1-18 0c0-6 4-9 9-17z" fill="#E1061A"/>'),
 "onde-fica": ("ONDE FICA", '<path d="M50 8a28 28 0 0 0-28 28c0 22 28 54 28 54s28-32 28-54A28 28 0 0 0 50 8z" fill="#fff"/><circle cx="50" cy="36" r="11" fill="#E1061A"/>'),
 "horario": ("HORÁRIO", '<circle cx="50" cy="50" r="38" fill="none" stroke="#fff" stroke-width="8"/><path d="M50 26v26l16 10" fill="none" stroke="#FFC72C" stroke-width="8" stroke-linecap="round"/>'),
 "clientes": ("CLIENTES", '<path d="M50 86S12 62 12 36a19 19 0 0 1 38-6 19 19 0 0 1 38 6c0 26-38 50-38 50z" fill="#fff"/><path d="M50 30l5 11 12 1-9 8 3 12-11-6-11 6 3-12-9-8 12-1z" fill="#FFC72C"/>'),
}
HTML = """<html><head><meta charset=utf-8><style>*{margin:0}body{width:1080px;height:1920px;display:flex;align-items:center;justify-content:center;
background:radial-gradient(circle at 50%% 45%%,#F2283A 0%%,#E1061A 40%%,#A30F1C 100%%);font-family:Montserrat}
.c{width:640px;height:640px;border-radius:50%%;background:rgba(0,0,0,.12);box-shadow:inset 0 0 0 14px rgba(255,255,255,.9);display:flex;flex-direction:column;align-items:center;justify-content:center}
svg{width:300px;height:300px}b{margin-top:22px;color:#fff;font-family:Anton;font-size:64px;letter-spacing:2px}</style></head>
<body><div class=c><svg viewBox="0 0 100 100">%s</svg><b>%s</b></div></body></html>"""
out = pathlib.Path(__file__).parent / "capas"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for nome, (txt, svg) in ICONES.items():
        pg.set_content(HTML % (svg, txt)); pg.screenshot(path=str(out / f"capa-{nome}.png"))
    b.close()
