---
name: motion-reel
description: Transforma fotos reais deitadas da Brasilgás (fachada, letreiro PARAGÁS, banner do Gás do Povo, estoque) em Reel vertical 1080x1920 com a câmera deslizando e aproximando até o que importa, com o véu vermelho, os textos e o botão do WhatsApp da marca. Use quando a peça for reel e não houver vídeo gravado, ou quando a foto for de paisagem e perder o letreiro no recorte vertical.
---

# Motion Reel (Brasilgás)

Por que existe: as fotos de fachada foram tiradas deitadas e de longe. No recorte vertical de post e story, o letreiro PARAGÁS fica de fora e sobra muro vermelho. Num vídeo, a câmera pode **deslizar pela foto até o letreiro**, aproveitando o material. (Decidido com o Gabriel em 23/11/2026.)

## Quando usar
- Dias de reel (terça e sexta na pauta) sem vídeo novo gravado.
- Fotos com `"motion_reel": true` em `fotos/catalogo.json`: as 6 fachadas bloqueadas para post e story, mais a da frente com o Gás do Povo. A foto de estoque P13 prata serve como fundo da cena final.
- A cada lote novo de fotos: ver quais são deitadas e de longe → marcar `motion_reel: true` e `foco_letreiro` no catálogo.
- Vídeo com pessoa real falando pra câmera engaja mais. Quando houver, ele vem primeiro, e o Motion Reel fica como complemento.

## Como montar (3 a 5 cenas, 12 a 18 s)
Siga o método 4 de `skills/brasilgas-conteudo/prompts-crescimento.md` (storyboard de retenção):
1. **INTERRUPÇÃO (0–3 s):** a foto mais reconhecível (a esquina), com a câmera indo do muro ao letreiro e um gancho curto (pergunta ou contraste).
2. **CURIOSIDADE / ENTREGA:** uma cena por benefício. Exemplos: revenda autorizada Paragás (letreiro), Gás do Povo (banner da frente), estoque (P13 prata).
3. **AÇÃO (última cena, a mais longa):** CTA com o botão do WhatsApp e o rodapé (`CTA` + `SUB`, sem `SEM_CTA`).

Regras de câmera (`DE` → `PARA`, coordenadas de 0 a 1 na foto; `zoom` 1 = altura inteira da foto):
- termine cada cena com o `foco_letreiro` do catálogo como centro do `PARA`, para o letreiro chegar à faixa clara do meio do quadro;
- `zoom` de 1.0 a 1.6, nunca mais que isso (a foto tem 1600 px e amolece se aproximar demais);
- o movimento é sempre suave (ease in-out) e a fusão entre cenas dura 0,5 s; o texto troca no meio da fusão;
- manchete de até 40 caracteres por cena, sem deixar palavra sozinha na linha (veja o quadro antes de renderizar).

## Comandos
```bash
python3 motion_reel.py midia/<data>/reel-x.json midia/<data>/reel-x.mp4
# gera reel-x.mp4 + reel-x-capa.png (+ .layout.json)
# validar: um spec por cena (KICKER/HEADLINE/SUB/CTA) + capa + legenda + alt
python3 validate.py --formato reel --spec cena0.json --spec cena1.json ... --imagem midia/<data>/reel-x-capa.png --legenda reel-x.txt --alt reel-x-alt.txt
```
Antes de renderizar o vídeo inteiro (cerca de 1 minuto), confira os quadros-chave: o início e o fim de cada cena. Depois do render, extraia 4 a 6 quadros com ffmpeg e abra com Read.

## Metricool
- `instagramData.type: "REEL"`, `media: [url do .mp4]`, `videoThumbnailUrl`: url da capa.
- Música: `audioConfiguration` (ver `musicas.json`). Se for rejeitada, publique sem música e registre.
- Foto real tratada (sem IA) → `isAiGenerated: false`.
- `mediaAltText` descreve cena por cena, com os textos que aparecem.
