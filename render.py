"""Renderiza artes Brasilgás a partir do template HTML (feed 1080x1350 ou story 1080x1920)."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).parent
LAYOUT = {
    # PT/PB: margens de segurança (no story, a interface do Instagram cobre topo e base)
    "feed":  dict(W=1080, H=1350, PT=56, PB=44, GAP1=46, HSIZE=104, HW=900, SSIZE=32, SW=860, IPAD=24, BMAX=700),
    "story": dict(W=1080, H=1920, PT=210, PB=240, GAP1=96, HSIZE=128, HW=920, SSIZE=36, SW=880, IPAD=30, BMAX=860),
}

def render(spec, out, fmt="feed"):
    html = (BASE / "templates/post.html").read_text()
    vals = {**LAYOUT[fmt], **spec}
    ilu = spec.get("ILUSTRACAO", "botijao")   # botijao | galao | combo
    vals["ILUSTRACAO_SVG"] = (BASE / "templates/ilustracoes" / f"{ilu}.svg").read_text()
    extra = ""
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
        pg.screenshot(path=out, type="png")
        # relatório de layout: caixas visíveis, para o validate.py achar sobreposição/estouro
        boxes = pg.evaluate("""() => {
          const o = {};
          for (const s of ['.top','.kicker','h1','.sub','.bot svg','.cta','.foot']) {
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
