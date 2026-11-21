"""Verificador automático da Brasilgás. Roda ANTES de mandar qualquer peça ao Metricool.

Uso:
  python3 validate.py --formato post|story|carrossel|reel --spec spec.json [--spec slide2.json ...] \
      [--imagem arte.png ...] [--legenda legenda.txt] [--alt alt.txt]

Sai com código 0 se passou e 1 se reprovou, imprimindo cada problema.
A tarefa diária deve corrigir e rodar de novo (até 3 tentativas). Se ainda reprovar,
o rascunho vai como draft:true e o Gabriel é avisado.
"""
import argparse, json, re, sys, pathlib

TELEFONES = ["(91) 98222-7035", "(91) 98548-0434"]
PROIBIDO = [
    (r"R\$\s*\d", "preço (R$)"),
    (r"\b\d+\s*%", "porcentagem/desconto"),
    (r"\bdesconto", "desconto"),
    (r"\bcupom", "cupom"),
    (r"\bpromo(ção|cao)\b", "promoção"),
    (r"\bgr[áa]tis\b", "grátis"),
    (r"\bsorteio", "sorteio"),
    (r"\bbrinde", "brinde"),
    (r"z[ée]\s*delivery", "Zé Delivery"),
    (r"\bifood\b", "iFood"),
    (r"\bem\s+\d+\s*min", "prazo de entrega"),
    (r"l[ée]o\s*g[áa]s", "nome de concorrente"),
    (r"\bsupergasbras|\bultragaz|\bliquig[áa]s|\bcopagaz", "outra distribuidora"),
]
HORARIO_OK = re.compile(r"7h\s*(às|a|–|-)\s*20h", re.I)
FERIADO_OK = re.compile(r"7h\s*(às|a|–|-)\s*13h", re.I)
LIMITES = {"KICKER": 30, "HEADLINE": 40, "SUB": 110, "CTA": 40}
# só para avisar; a regra de quais ofertas valem está em ofertas.json
def ofertas_confirmadas():
    try:
        return json.loads(pathlib.Path(__file__).with_name("ofertas.json").read_text()).get("ofertas_confirmadas", [])
    except Exception:
        return []

def checar_texto(txt, onde, erros, permitir_oferta):
    low = txt.lower()
    for padrao, nome in PROIBIDO:
        if permitir_oferta and nome in ("desconto", "promoção", "porcentagem/desconto"):
            continue
        if re.search(padrao, low, re.I):
            erros.append(f"{onde}: contém {nome}")
    # telefone no formato 9xxxx que não seja oficial
    for tel in re.findall(r"9\d{4}[-\s]?\d{4}", txt):
        dig = re.sub(r"\D", "", tel)
        if dig not in ("982227035", "985480434"):
            erros.append(f"{onde}: telefone desconhecido {tel}")
    # horário errado (ex.: 7h às 18h)
    for h in re.findall(r"7h\s*(?:às|a|–|-)\s*(\d{1,2})h", txt):
        if h not in ("20", "13"):
            erros.append(f"{onde}: horário diferente do oficial (7h às {h}h)")

def checar_layout(img, erros):
    lay = pathlib.Path(str(img) + ".layout.json")
    if not lay.exists():
        erros.append(f"{img}: sem relatório de layout (renderize com render.py)")
        return
    d = json.loads(lay.read_text())
    W, H, bx = d["W"], d["H"], d["boxes"]
    for nome, (l, t, r, b) in bx.items():
        if l < 0 or t < 0 or r > W + 1 or b > H + 1:
            erros.append(f"{img}: '{nome}' sai da arte")
    textos = [k for k in bx if k != ".bot"]
    pares = [(a, c) for i, a in enumerate(textos) for c in textos[i + 1:]]
    pares += [(".bot", k) for k in textos if ".bot" in bx and k not in (".top",)]
    for a, c in pares:
        if a not in bx or c not in bx:
            continue
        A, C = bx[a], bx[c]
        ix = min(A[2], C[2]) - max(A[0], C[0])
        iy = min(A[3], C[3]) - max(A[1], C[1])
        if ix > 4 and iy > 4:
            erros.append(f"{img}: '{a}' sobrepõe '{c}'")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formato", required=True, choices=["post", "story", "carrossel", "reel"])
    ap.add_argument("--spec", action="append", default=[])
    ap.add_argument("--imagem", action="append", default=[])
    ap.add_argument("--legenda")
    ap.add_argument("--alt")
    a = ap.parse_args()
    erros, avisos = [], []
    permitir_oferta = bool(ofertas_confirmadas())

    for sp in a.spec:
        spec = json.loads(pathlib.Path(sp).read_text())
        for campo, lim in LIMITES.items():
            v = str(spec.get(campo, ""))
            if campo in ("KICKER", "HEADLINE") and not v:
                erros.append(f"{sp}: {campo} vazio")
            if len(v) > lim:
                erros.append(f"{sp}: {campo} com {len(v)} caracteres (máx. {lim})")
        checar_texto(" ".join(str(spec.get(k, "")) for k in LIMITES), sp, erros, permitir_oferta)

    for img in a.imagem:
        checar_layout(img, erros)

    if a.formato in ("post", "carrossel", "reel"):
        if not a.legenda:
            erros.append("legenda obrigatória para post/carrossel/reel")
        else:
            leg = pathlib.Path(a.legenda).read_text()
            checar_texto(leg, "legenda", erros, permitir_oferta)
            for tel in TELEFONES:
                if tel not in leg:
                    erros.append(f"legenda: falta o WhatsApp {tel}")
            if not HORARIO_OK.search(leg) or not FERIADO_OK.search(leg):
                erros.append("legenda: falta o horário (7h às 20h e 7h às 13h)")
            if "Alameda Padre Rolim" not in leg:
                erros.append("legenda: falta o endereço")
            n_hash = len(re.findall(r"#\w+", leg))
            if not 3 <= n_hash <= 5:
                erros.append(f"legenda: {n_hash} hashtags (o Instagram aceita no máximo 5; use de 3 a 5)")
            primeira = leg.strip().splitlines()[0] if leg.strip() else ""
            if len(primeira) > 90:
                avisos.append("gancho (1ª linha) longo demais: o Instagram corta em ~90 caracteres")
    if not a.alt or not pathlib.Path(a.alt).read_text().strip():
        erros.append("mediaAltText (descrição da arte) obrigatório")

    for w in avisos:
        print("AVISO:", w)
    if erros:
        for e in erros:
            print("ERRO:", e)
        print(f"REPROVADO ({len(erros)} problema(s))")
        sys.exit(1)
    print("APROVADO")

if __name__ == "__main__":
    main()
