"""Foto de perfil 1080x1080 com o logo oficial (legível no círculo pequeno)."""
import pathlib
from playwright.sync_api import sync_playwright
BOT = (pathlib.Path(__file__).parent.parent / "templates/ilustracoes/botijao.svg").read_text()
CSS = """*{margin:0;box-sizing:border-box}body{width:1080px;height:1080px;display:flex;align-items:center;justify-content:center;font-family:Montserrat}"""
OPC = {
 # A: fundo vermelho, logo empilhado em caixa branca
 "A": CSS + """body{background:radial-gradient(circle at 50% 40%,#F2283A,#E1061A 50%,#A30F1C)}
  .box{background:#fff;border-radius:60px;padding:46px 60px 50px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.25)}
  .w{font-weight:900;line-height:.92;color:#1D4FA3;font-size:150px;letter-spacing:2px}.w i{font-style:normal;color:#E1061A}
  .p{margin-top:22px;background:#E1061A;color:#fff;font-weight:800;font-size:62px;letter-spacing:8px;padding:10px 20px;border-radius:10px}""",
 # B: fundo branco, logo em linha com botijão
 "B": CSS + """body{background:#fff;flex-direction:column}
  .ic{width:260px;margin-bottom:10px}.ic svg{width:100%;height:auto}
  .w{font-weight:900;color:#1D4FA3;font-size:112px;letter-spacing:1px;line-height:1}.w i{font-style:normal;color:#E1061A}
  .p{margin-top:20px;background:#E1061A;color:#fff;font-weight:800;font-size:52px;letter-spacing:8px;padding:8px 36px;border-radius:10px;text-align:center}""",
}
HTML = {"A": '<div class="box"><div class="w">BRASIL<br><i>GÁS</i></div><div class="p">PARAGÁS</div></div>',
        "B": f'<div class="ic">{BOT}</div><div class="w">BRASIL<i>GÁS</i></div><div class="p">PARAGÁS</div>'}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for k in OPC:
        pg.set_content(f"<html><head><meta charset=utf-8><style>{OPC[k]}</style></head><body>{HTML[k]}</body></html>")
        pg.screenshot(path=str(pathlib.Path(__file__).parent / f"foto-perfil-{k}.png"))
    b.close()
