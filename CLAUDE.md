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

## Calendário inteligente (verificar TODO dia, antes da pauta)
- Ler `calendario.json`. Para cada evento, cada janela "D-N:formato" vence na data (evento − N dias). Se vence hoje e `historico.json` ainda não tem `evento` = "<id>:<janela>", produzir essa peça.
- Evento do calendário tem prioridade sobre a pauta do dia. Máximo de 2 rascunhos por dia (1 do calendário + 1 da pauta, ou 2 do calendário).
- tipo "feriado": usar o horário especial 7h–13h (regra da revenda). "ponto_facultativo": não afirmar horário. "cultural"/"comercial": horário normal.
- Story de véspera (D-1) agendar entre 17h e 19h. Story do dia (D0) agendar às 7h.
- Datas regionais têm peso: Círio (maniçoba cozinha por dias, então o gás não pode faltar), Semana Santa, quadra junina, Aniversário de Castanhal (28/01), Adesão do Pará (15/08).
- Em dezembro, completar o calendário do ano seguinte (regras de cálculo em `_manutencao`) e avisar o Gabriel.

## Carrossel
- Formato "carrossel": de 3 a 5 slides em feed (1080x1350). Os slides do meio usam `"SEM_CTA": true` e `"NUMERO": "2/5"`. O último slide tem CTA. Pode usar `"SEM_BOTIJAO": true` para variar.
- No Metricool é um POST com várias URLs em `media`, na ordem.
- Ideias que funcionam no @souparagas: histórias em sequência ("contos da cozinha sem gás"), comidas típicas por data, homenagens.

## Aprendizados dos prints (19/11/2026)
- Logo real: "BRASIL" azul + "GÁS" vermelho, sobre faixa vermelha "PARAGÁS" com selo azul, numa caixa branca. O template reproduz isso em texto até chegar o arquivo do logo.
- Mascote prata (botijão com olhos) já é usado pela marca e o público reconhece.
- No Leo Gás, o que mais engaja é atendente real falando pra câmera (com fundo trocado), muito mais que arte feita só com IA. Priorizar rosto humano nos Reels quando houver fotos ou vídeos em `fotos/`.
- Se usar imagem gerada por IA, marcar isAiGenerated:true no Metricool.

## Referência visual @souparagas (confirmado com Gabriel em 19/11/2026)
- Horário confirmado: seg–sáb 7h–20h; domingos e feriados 7h–13h.
- A Brasilgás NÃO atende pelo Zé Delivery e não participa de cupons da Paragás. Nunca citar Zé Delivery, app de terceiros ou cupom da Paragás.
- Do @souparagas usar só a linguagem visual: vermelho com amarelo de destaque, faixa "PARAGÁS", apelido "Pratinha" para o botijão prata, carrosséis com história, comidas típicas por data, homenagens em datas comemorativas.
