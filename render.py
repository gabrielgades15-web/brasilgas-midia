"""Renderiza artes Brasilgás a partir do template HTML (feed 1080x1350, quadrado 1080x1080 ou story 1080x1920)."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).parent
LAYOUT = {
    # PT/PB: margens de segurança (no story, a interface do Instagram cobre topo e base)
    "feed":  dict(W=1080, H=1350, PT=56, PB=44, GAP1=58, CSIZE=64, CSUB=28, HSIZE=104, HW=900, SSIZE=32, SW=860, IPAD=24, BMAX=700),
    # quadrado: anúncio do WhatsApp (1:1). PB alto: o botão "WhatsApp" do anúncio cobre o canto de baixo
    "quadrado": dict(W=1080, H=1080, PT=36, PB=150, GAP1=26, CSIZE=50, CSUB=22, HSIZE=86, HW=960, SSIZE=26, SW=900, IPAD=16, BMAX=420),
    "story": dict(W=1080, H=1920, PT=210, PB=240, GAP1=110, CSIZE=72, CSUB=30, HSIZE=128, HW=920, SSIZE=36, SW=880, IPAD=30, BMAX=860),
}

VEU = ("linear-gradient(180deg,rgba(163,15,28,.95) 0%,rgba(200,6,26,.80) 32%,rgba(225,6,26,.06) 50%,"
       "rgba(120,8,20,.15) 62%,rgba(110,6,18,.94) 84%)")

def render(spec, out, fmt="feed", overlay=False):
    """overlay=True: PNG transparente (só véu + textos), usado pelo motion_reel.py por cima da foto em movimento."""
    html = (BASE / "templates/post.html").read_text()
    import base64 as _b64   # logo oficial vetorial (Brasilgás + bandeira Paragás), desde 25/11
    html = html.replace("{{LOGO_SRC}}", "data:image/svg+xml;base64," + _b64.b64encode((BASE / "logo/brasilgas-logo-caixa.svg").read_bytes()).decode())
    vals = {**LAYOUT[fmt], **spec}
    ilu = spec.get("ILUSTRACAO", "botijao")   # botijao | galao | combo
    vals["ILUSTRACAO_SVG"] = (BASE / "templates/ilustracoes" / f"{ilu}.svg").read_text()
    extra = ""
    if spec.get("FOTO"):   # foto real de fundo, com véu vermelho por cima para o texto ler bem
        import base64
        from tratar_foto import tratar
        b64 = base64.b64encode(tratar(BASE / spec["FOTO"]).read_bytes()).decode()
        extra += ("body{background:linear-gradient(180deg,rgba(163,15,28,.95) 0%%,rgba(200,6,26,.80) 32%%,rgba(225,6,26,.06) 50%%,"
                  "rgba(120,8,20,.15) 62%%,rgba(110,6,18,.94) 84%%),url(data:image/jpeg;base64,%s) center/cover}" % b64)
        if not spec.get("ILUSTRACAO"):
            extra += ".ilu{visibility:hidden}"
        extra += ".texto .sub{display:none}.sub2{display:block}"   # frase desce para a base da foto
        if not spec.get("SUB"):
            extra += ".sub2{display:none}"   # sem frase: a foto respira (ex.: anúncio quadrado)
    if overlay:   # sem foto: véu vermelho translúcido + textos, fundo transparente
        extra += "html,body{background:transparent!important}body{background-image:%s!important}" % VEU
        if not spec.get("ILUSTRACAO"):
            extra += ".ilu{visibility:hidden}"
        extra += ".texto .sub{display:none}.sub2{display:block}"
        if not spec.get("SUB"):
            extra += ".sub2{visibility:hidden}"
    if spec.get("SEM_CTA"):      # slides do meio do carrossel
        extra += ".cta,.foot{display:none}"
    if spec.get("SEM_BOTIJAO"):
        extra += ".ilu{visibility:hidden}"
    if spec.get("NUMERO"):       # marcador do slide, ex. "2/5"
        extra += ".kicker::after{content:'  %s';opacity:.6}" % spec["NUMERO"]
    html = html.replace("</style>", extra + "</style>")
    for k, v in vals.items():
        html = html.replace("{{%s}}" % k, str(v))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": vals["W"], "height": vals["H"]})
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=out, type="png", omit_background=overlay)
        # relatório de layout: caixas visíveis, para o validate.py achar sobreposição/estouro
        boxes = pg.evaluate("""() => {
          const o = {};
          for (const s of ['.top','.kicker','h1','.sub','.sub2','.bot svg','.cta','.foot']) {
            const e = document.querySelector(s);
            if (!e || getComputedStyle(e).display === 'none') continue;
            const r = e.getBoundingClientRect();
            o[s] = [r.left, r.top, r.right, r.bottom];
          }
          return o;
        }""")
        b.close()
    pathlib.Path(str(out) + ".layout.json").write_text(json.dumps({"W": vals["W"], "H": vals["H"], "boxes": boxes}))

if __name__ == "__main__":
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    render(spec, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "feed")
