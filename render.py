"""Renderiza artes Brasilgás a partir do template HTML (feed 1080x1350 ou story 1080x1920)."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).parent
LAYOUT = {
    "feed":  dict(TTOP=50, W=1080, H=1350, KTOP=235, HTOP=300, HW=600, HSIZE=112, STOP=670, BRIGHT=40, BBOT=280, BW=360, CBOT=110, FBOT=50),
    "story": dict(TTOP=220, W=1080, H=1920, KTOP=400, HTOP=475, HW=900, HSIZE=132, STOP=775, BRIGHT=330, BBOT=500, BW=340, CBOT=300, FBOT=230),
}

def render(spec, out, fmt="feed"):
    html = (BASE / "templates/post.html").read_text()
    vals = {**LAYOUT[fmt], **spec}
    ilu = spec.get("ILUSTRACAO", "botijao")   # botijao | galao | combo
    vals["ILUSTRACAO_SVG"] = (BASE / "templates/ilustracoes" / f"{ilu}.svg").read_text()
    if ilu == "combo":
        if fmt == "story":
            vals["BW"] = 760
            vals["BRIGHT"] = (vals["W"] - vals["BW"]) // 2
        else:  # feed: combo menor, encostado à direita, abaixo do texto
            vals["BW"], vals["BRIGHT"] = 380, 30
    elif ilu == "galao":
        vals["BW"] = int(vals["BW"] * 1.05)
    extra = ""
    if spec.get("SEM_CTA"):      # slides do meio do carrossel
        extra += ".cta,.foot{display:none}"
    if spec.get("SEM_BOTIJAO"):
        extra += ".bot{display:none}"
    if spec.get("NUMERO"):       # marcador do slide, ex. "2/5"
        extra += ".kicker::after{content:'  %s';opacity:.6}" % spec["NUMERO"]
    html = html.replace("</style>", extra + "</style>")
    for k, v in vals.items():
        html = html.replace("{{%s}}" % k, str(v))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": vals["W"], "height": vals["H"]})
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=out, type="png")
        # relatório de layout: caixas visíveis, para o validate.py achar sobreposição/estouro
        boxes = pg.evaluate("""() => {
          const o = {};
          for (const s of ['.top','.kicker','h1','.sub','.bot','.cta','.foot']) {
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
