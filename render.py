"""Renderiza artes Brasilgás a partir do template HTML (feed 1080x1350 ou story 1080x1920)."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).parent
LAYOUT = {
    "feed":  dict(TTOP=60, W=1080, H=1350, KTOP=200, HTOP=270, HW=600, HSIZE=118, STOP=660, BRIGHT=40, BBOT=250, BW=380, CBOT=110, FBOT=50),
    "story": dict(TTOP=220, W=1080, H=1920, KTOP=400, HTOP=475, HW=900, HSIZE=132, STOP=775, BRIGHT=330, BBOT=500, BW=340, CBOT=300, FBOT=230),
}

def render(spec, out, fmt="feed"):
    html = (BASE / "templates/post.html").read_text()
    vals = {**LAYOUT[fmt], **spec}
    for k, v in vals.items():
        html = html.replace("{{%s}}" % k, str(v))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": vals["W"], "height": vals["H"]})
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=out, type="png")
        b.close()

if __name__ == "__main__":
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    render(spec, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "feed")
