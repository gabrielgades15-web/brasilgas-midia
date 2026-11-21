---
name: brasilgas-conteudo
description: Cria artes, legendas, carrosséis, stories e roteiros de Reels para o Instagram da Brasilgás (revenda autorizada Paragás em Castanhal-PA), seguindo as regras da marca, o calendário regional e o foco em pedidos pelo WhatsApp.
---

# Conteúdo Brasilgás

Use esta skill sempre que for produzir qualquer peça para o @brasilgas_caicara (antigo @brasilgas7035): arte de post, story, carrossel, Reel, legenda, gancho, hashtags ou ideia de pauta.

## 0. Plugins de apoio (use quando estiverem disponíveis na sessão)
Antes de escrever, veja se as skills dos plugins **Marketing** (Anthropic) e **Social Media Skills** estão listadas. Se estiverem, carregue as que servem para a peça do dia e aplique o método delas. **As regras desta skill sempre vencem em caso de conflito** (preço, dados de contato, tom, P13 prata).

| Peça | Skills de apoio (Social Media Skills) | Marketing |
|---|---|---|
| Qualquer peça | hook-writer, writing-style-and-tone | voz da marca |
| Legenda de post/reel | caption-writer, hashtag-strategy, instagram-seo | criação de conteúdo |
| Carrossel | carousel-writer, storytelling-and-narrative | criação de conteúdo |
| Story | story-writer, interactive-content | — |
| Reel | reels-script, short-form-video-script, talking-head-and-piece-to-camera | — |
| Data comemorativa | seasonal-and-moment-marketing | planejamento de campanha |
| Arte/template | design-and-templates, quote-cards-and-text-graphics | — |
| Revisão semanal | analytics-and-reporting, competitor-analysis | desempenho e concorrentes |
| Conversa → pedido | social-selling-and-dm, link-in-bio-and-traffic | — |

Se os plugins não estiverem disponíveis, siga só esta skill: ela é suficiente.

## 1. Quem é a Brasilgás
- Revenda **autorizada Paragás** em Castanhal-PA. Vende gás P13 (botijão prata) e água mineral 20L, com entrega. Revenda credenciada do **Gás do Povo**.
- Objetivo de toda peça: **gerar conversa no WhatsApp que vira pedido.** Curtida é bônus.
- Público: famílias de Castanhal, donas e donos de casa, pequenos comércios (lanchonetes, restaurantes).

## 2. Regras não negociáveis
- **Nunca preço**, em arte ou legenda. Preço só no WhatsApp.
- **Nunca inventar** promoção, cupom, desconto, brinde, prazo de entrega ("em 30 min") ou sorteio. Oferta só se estiver em `ofertas.json`.
- **Nunca citar** Zé Delivery, apps de terceiros ou cupons da Paragás.
- **Água:** só "Água", "Água 20L" ou "Galão 20L". Nunca a marca da água (ela é dita no atendimento).
- Botijão sempre **prata, sem logo**. O mascote prata nunca aparece ao lado de um P13.
- Dados exatamente assim:
  - WhatsApp (91) 98222-7035 e (91) 98548-0434;
  - seg–sáb 7h–20h, domingos e feriados 7h–13h;
  - Alameda Padre Rolim, Castanhal.
- Feriado oficial: horário 7h–13h. Ponto facultativo (Carnaval, Corpus Christi): não afirmar horário.
- Concorrentes (Grupo Leo Gás) são só referência de formato. Nunca citar nome nem copiar arte ou texto.
- Imagem gerada por IA → `isAiGenerated: true` no Metricool.

## 3. Voz da marca
- **Vizinha prestativa de Castanhal**: próxima, rápida, confiável. Fala "a gente leva", "chama no zap", "pediu, chegou".
- Português do Pará do dia a dia, sem gíria forçada. Pode usar "égua" ou "maninho" no máximo uma vez por semana, e só em Reel ou story.
- Frases curtas. Verbo no imperativo no CTA: **Chame, Peça, Garanta**.
- Emoji com moderação: no máximo 4 por legenda (🔥📲🕖📍 são os de sempre).
- Diferenciais que podem ser ditos: revenda autorizada Paragás, botijão prata original, Gás do Povo, atende domingo de manhã, entrega em casa, água 20L junto.

## 4. Ganchos (primeira linha da legenda e texto grande da arte)
Escolha uma fórmula e não repita a mesma em menos de 7 dias:
1. **Dor do momento:** "O gás acabou no meio do almoço?"
2. **Pergunta direta:** "Você sabe quanto tempo dura um P13?"
3. **Urgência leve:** "Não deixe pra última hora: amanhã é feriado."
4. **Prova local:** "Castanhal inteira já conhece o botijão prata."
5. **Benefício:** "Pediu no zap, chegou na sua porta."
6. **Curiosidade/dica:** "3 sinais de que seu gás está acabando."
7. **Data/cultura:** "Maniçoba cozinha por dias. Seu gás aguenta?"

Manchete da arte: **até 40 caracteres**, com no máximo 3 linhas na arte.

## 5. Legenda (post, carrossel, reel)
```
[Gancho, 1 linha + 1 emoji]

[2 a 3 linhas de benefício ou história, falando com "você"]
[1 linha de diferencial: revenda autorizada Paragás / Gás do Povo / domingo aberto]

📲 Chame no WhatsApp: (91) 98222-7035 ou (91) 98548-0434
🕖 Seg a sáb, 7h às 20h | Domingos e feriados, 7h às 13h
📍 Alameda Padre Rolim, Castanhal

#Castanhal #GásDeCozinha #Brasilgás + até 2 do tema (MÁXIMO 5 hashtags: limite do Instagram desde dez/2025)
```
- A busca do Instagram hoje é por palavra-chave: coloque "gás em Castanhal" / "entrega de gás" escrito na legenda.
- Hashtags do tema: #GásDoPovo #EntregaDeGás #ÁguaMineral #CírioDeNazaré #Pará #GásCastanhal.
- Feriado: acrescente na linha do horário "(hoje, feriado, até 13h)".
- Preencha sempre `mediaAltText` com a descrição da arte e o texto que aparece nela.

## 6. Formatos

### Post (feed 1080x1350)
Spec: KICKER (até 30, a faixa amarela), HEADLINE (até 40), SUB (até 110), CTA (até 40). Renderize com `render.py ... feed`.

### Story (1080x1920)
Uma ideia só. O texto da arte é tudo, porque story não tem legenda. Véspera de feriado entre 17h e 19h; no dia, às 7h.

### Carrossel (3 a 5 slides em feed)
Estrutura que funciona (inspirada no @souparagas):
1. **Capa:** gancho + promessa ("Contos da cozinha sem gás").
2-4. **Desenvolvimento:** uma cena ou dica por slide, com `SEM_CTA: true` e `NUMERO: "n/total"`.
5. **Fechamento:** virada + CTA ("Peça antes do pesadelo acontecer").
Ideias:
- histórias da cozinha (arroz pela metade, visita chegando, chama apagando);
- "3 sinais que o gás está acabando";
- "Como usar o Gás do Povo em 3 passos";
- comidas típicas da data (maniçoba, pato no tucupi, peixe da Semana Santa, comidas juninas).

### Reel (12 a 18 s, 1080x1920)
- Roteiro em 4 telas: **gancho (0–3 s) → problema → solução Brasilgás → CTA com WhatsApp**.
- Se houver fotos ou vídeos reais em `fotos/`, eles vêm primeiro. **Rosto humano engaja muito mais** (no Leo Gás, atendente falando pra câmera teve de 2 a 3 vezes mais curtidas que arte só de IA).
- Roteiro de fala para gravação (talking head, 15–30 s):
  "Seu gás acabou? Calma! Chama a Brasilgás no WhatsApp [mostra o número] que a gente leva o botijão prata Paragás até sua casa. Aqui em Castanhal, de segunda a sábado até 8 da noite e domingo até 1 da tarde."

## 7. Pilares da semana (pauta.json)
- segunda: entrega e atendimento
- terça: humanização (Reel)
- quarta: segurança e dicas
- quinta: Gás do Povo
- sexta: urgência e fim de semana (Reel)
- sábado: água 20L e combo
- domingo: domingo aberto

Datas de `calendario.json` têm prioridade sobre a pauta.

## 8. Checklist antes de enviar ao Metricool
- [ ] Sem preço, sem promoção inventada, sem Zé Delivery.
- [ ] Telefones, horário e endereço exatamente como na seção 2.
- [ ] P13 prata, mascote longe do P13.
- [ ] Manchete com até 40 caracteres, texto sem sobreposição (abri a imagem e conferi).
- [ ] Português revisado (acentos: Gás, Paragás, Castanhal, Círio).
- [ ] Legenda no formato da seção 5 (post/carrossel/reel) e `mediaAltText` preenchido.
- [ ] Rascunho (`draft: true`), nunca publicação direta.
- [ ] Gancho diferente dos últimos 7 dias (`historico.json`).
