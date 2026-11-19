# Brasilgás — produção diária de conteúdo

Repositório usado pela tarefa agendada diária. As artes ficam em `midia/AAAA-MM-DD/` e o Metricool lê pelos links raw públicos.

## Regras de marca (não negociáveis)
- Preço NUNCA aparece em arte nem legenda (preço só no WhatsApp).
- Botijão P13 sempre prata, sem logo. Mascote prata e P13 nunca lado a lado.
- Brasilgás é revenda autorizada; Paragás é a marca do gás.
- Dados fixos: WhatsApp (91) 98222-7035 e 98548-0434; seg–sáb 7h–20h, domingos e feriados 7h–13h; Alameda Padre Rolim, Castanhal.
- Gás do Povo: revenda credenciada (pode citar).
- Nunca inventar promoção, cupom, desconto, prazo de entrega ou preço. Se a pauta pedir oferta e não houver oferta confirmada em `ofertas.json`, troque por outro tema.
- Conteúdo original. O Grupo Leo Gás é só referência de formato.

## Fluxo diário
1. Ler `pauta.json` e escolher o tema do dia da semana (fuso America/Belem). Evitar repetir manchete dos últimos 14 dias (`historico.json`).
2. Escrever o spec (KICKER, HEADLINE, SUB, CTA) e renderizar: `python3 render.py spec.json saida.png feed|story`.
3. Conferir a imagem (ler o PNG) antes de seguir.
4. Commit + push em `midia/AAAA-MM-DD/`.
5. Criar RASCUNHO no Metricool (blogId 7861236, draft:true, autoPublish:true) no melhor horário do dia, com legenda + CTA + hashtags locais.
6. Atualizar `historico.json`.
