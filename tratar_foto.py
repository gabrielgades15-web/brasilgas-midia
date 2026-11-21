"""Tratamento leve das fotos reais antes de entrar nas artes.

Deixa a foto mais bonita sem parecer falsa: corrige exposição, dá um pouco de contraste,
saturação moderada (céu mais azul, vermelho da fachada mais vivo), nitidez e vinheta suave.
Não remove marcas de uso dos botijões (são reais) e não mexe em formas.

Uso: python3 tratar_foto.py fotos/original.jpg  → grava fotos/tratadas/original.jpg
O render.py chama isso sozinho quando o spec tem "FOTO".
"""
import sys, pathlib
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw

BASE = pathlib.Path(__file__).parent


def tratar(origem: pathlib.Path) -> pathlib.Path:
    destino = origem.parent / "tratadas" / origem.name
    if destino.exists() and destino.stat().st_mtime >= origem.stat().st_mtime:
        return destino
    destino.parent.mkdir(exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(origem)).convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=1)            # corrige céu estourado / sombra lavada
    im = ImageEnhance.Brightness(im).enhance(1.03)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.15)           # cor viva, sem exagero
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=3))  # metal do P13 mais nítido
    # vinheta suave: escurece as bordas e leva o olho ao centro
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((-w * .15, -h * .15, w * 1.15, h * 1.15), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(w, h) // 8))
    escuro = ImageEnhance.Brightness(im).enhance(0.72)
    im = Image.composite(im, escuro, mask)
    im.save(destino, quality=88)
    return destino


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(tratar(pathlib.Path(a)))
