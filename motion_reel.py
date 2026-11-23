"""Motion Reel da Brasilgás: transforma fotos deitadas (fachada, letreiro) em Reel vertical 1080x1920.

A "câmera" desliza e aproxima dentro de cada foto (pan + zoom suave), indo até o que importa
(letreiro PARAGÁS, banner do Gás do Povo), com o véu vermelho e os textos da marca por cima.
Assim a foto de paisagem, que perde o letreiro quando é recortada para o formato vertical, vira vídeo.

Uso: python3 motion_reel.py spec.json saida.mp4
Gera: saida.mp4 (30 fps, H.264 + faixa de áudio muda), saida-capa.png e saida-capa.png.layout.json
(a capa passa no validate.py como --imagem).

Spec:
{
  "TRANSICAO": 0.5,                       # segundos de fusão entre cenas
  "CENAS": [
    {"FOTO": "fotos/fachada-esquina-completa.jpg", "DUR": 4.5,
     "DE":   {"x": 0.62, "y": 0.50, "zoom": 1.0},   # centro do quadro (0-1 na foto) e zoom (1 = altura inteira)
     "PARA": {"x": 0.22, "y": 0.47, "zoom": 1.5},
     "KICKER": "...", "HEADLINE": "...", "SUB": "...", "CTA": "...", "SEM_CTA": true}
  ]
}
A última cena deve ter CTA (botão do WhatsApp + rodapé). As do meio usam SEM_CTA.
"""
import sys, json, math, pathlib, subprocess, tempfile, shutil, os
from PIL import Image

BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
from render import render
from tratar_foto import tratar

W, H, FPS = 1080, 1920, 30


def suave(p):  # ease in-out
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, p)))


def quadro(foto, cam):
    """Recorta a foto na posição da câmera (float, sem tremer) e devolve 1080x1920."""
    fw, fh = foto.size
    h = fh / cam["zoom"]
    w = h * W / H
    if w > fw:                       # foto mais estreita que 9:16 nesse zoom
        w, h = fw, fw * H / W
    cx = min(max(cam["x"] * fw, w / 2), fw - w / 2)
    cy = min(max(cam["y"] * fh, h / 2), fh - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return foto.transform((W, H), Image.Transform.EXTENT, box, Image.Resampling.BICUBIC)


def cam_em(cena, p):
    a, b, k = cena["DE"], cena["PARA"], suave(p)
    return {c: a[c] + (b[c] - a[c]) * k for c in ("x", "y", "zoom")}


def main(spec_path, out):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    cenas, T = spec["CENAS"], float(spec.get("TRANSICAO", 0.5))
    tmp = pathlib.Path(tempfile.mkdtemp())
    for i, c in enumerate(cenas):
        c["_foto"] = Image.open(tratar(BASE / c["FOTO"])).convert("RGB")
        ov = tmp / f"ov{i}.png"
        render({k: v for k, v in c.items() if k.isupper() and k not in ("FOTO", "DE", "PARA", "DUR")}, str(ov), "story", overlay=True)
        c["_ov"] = Image.open(ov).convert("RGBA")
        c["_ovpath"] = ov
    inicios, t = [], 0.0
    for c in cenas:
        inicios.append(t)
        t += c["DUR"] - T
    total = t + T

    def foto_cena(i, tl):
        c = cenas[i]
        return quadro(c["_foto"], cam_em(c, tl / c["DUR"])).convert("RGBA")

    def frame_cena(i, tl):
        return Image.alpha_composite(foto_cena(i, tl), cenas[i]["_ov"]).convert("RGB")

    parcial = str(out) + ".parcial.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
           "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "64k", parcial]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(total * FPS))
    for f in range(n):
        tg = f / FPS
        ativos = [i for i, s in enumerate(inicios) if s <= tg < s + cenas[i]["DUR"]] or [len(cenas) - 1]
        i = ativos[0]
        if len(ativos) > 1:   # fusão só das fotos; o texto troca no meio da fusão (sem texto fantasma)
            j = ativos[1]
            k = (tg - inicios[j]) / T
            foto = Image.blend(foto_cena(i, tg - inicios[i]), foto_cena(j, tg - inicios[j]), k)
            im = Image.alpha_composite(foto, cenas[j if k >= 0.5 else i]["_ov"]).convert("RGB")
        else:
            im = frame_cena(i, min(tg - inicios[i], cenas[i]["DUR"]))
        pr.stdin.write(im.tobytes())
    pr.stdin.close()
    if pr.wait() != 0:
        sys.exit("ffmpeg falhou")
    os.replace(parcial, out)

    # capa = 1ª cena no ponto final da câmera (letreiro em destaque) + relatório de layout para o validate.py
    capa = str(out).rsplit(".", 1)[0] + "-capa.png"
    frame_cena(0, cenas[0]["DUR"]).save(capa)
    shutil.copy(str(cenas[0]["_ovpath"]) + ".layout.json", capa + ".layout.json")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{out} ({total:.1f}s, {n} quadros) + {capa}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
