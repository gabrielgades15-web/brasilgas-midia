# 7 métodos de crescimento (adaptados para a Brasilgás)

Origem: 7 prompts do @gurudoprompt que o Gabriel trouxe em 23/11/2026. Viraram métodos fixos do nosso trabalho.
As regras da Brasilgás (CLAUDE.md, aprendizados.md e SKILL.md) sempre vencem: preço nunca aparece, nada de promoção inventada e o atendimento é feito por pessoas.
Os 7 métodos têm uma regra em comum: **não inventar métricas, tendências nem resultados**. Quando um dado não existe (cliques no WhatsApp, vendas), ele fica marcado como "sem dado" e, se for o caso, pedimos o número ao Gabriel.

Contexto fixo para preencher os [CAMPOS] dos prompts originais:
- Perfil: @brasilgas_caicara · Nicho: revenda de gás P13 e água 20L em Castanhal-PA.
- Público: famílias de Castanhal e pequenos comércios.
- Produto: gás P13 Paragás (inclui Gás do Povo) e água 20L, com entrega.
- Objetivo: conversa no WhatsApp que vira pedido. Preço: nunca no conteúdo.
- Ferramentas: Metricool (agenda e métricas), GitHub (artes), WhatsApp (atendimento humano).

## Quando cada método roda

| # | Método | Quando roda | Onde fica o resultado |
|---|---|---|---|
| 1 | Analisar o Instagram (auditoria por evidências) | 1º domingo do mês, na rodada das 20h34 | `relatorios/auditoria-AAAA-MM.md` |
| 2 | Encontrar ideias (engenharia reversa da demanda) | 1º domingo do mês, junto com o 1 | `banco-de-pautas.json` |
| 3 | Carrossel (engenharia reversa da promessa) | sempre que a peça for carrossel | spec dos slides + legenda |
| 4 | Reel (storyboard de retenção) | sempre que a peça for reel | roteiro em `midia/AAAA-MM-DD/` |
| 5 | Planejar 7 dias (planejamento por restrições) | todo domingo, na rodada das 20h34 | `plano-semana.json` |
| 6 | Seguidor → cliente (funil por estados) | revisão mensal, com o 1; e em toda legenda (CTA) | seção "Funil" da auditoria |
| 7 | Aumentar alcance e vendas (ciclo de aprendizado) | segunda de manhã, na leitura semanal | relatório da semana + `aprendizados.md` |

---

## 1. Analisar o Instagram: auditoria por evidências (mensal)
- Dados: últimos 30 posts, ou o que houver, tirados de `metricas_posts.csv` e do Metricool: views, alcance, curtidas, comentários, salvamentos e compartilhamentos.
- Separe as peças em 3 grupos: **ATRAÇÃO** (alcance de não seguidores, views), **ENGAJAMENTO** (comentários, salvos, compartilhamentos) e **CONVERSÃO** (conversas no WhatsApp, quando o Gabriel informar).
- Compare cada peça com a **mediana do próprio perfil**, nunca com médias de mercado.
- Encontre 5 oportunidades desperdiçadas: tema bom com formato fraco, horário ruim, CTA ausente, foto real pouco usada etc.
- Classifique tema, manchete, formato e CTA em **repetir, corrigir ou abandonar**. Separe o que é padrão observado do que ainda é hipótese.
- Entregue: diagnóstico + 7 recomendações + plano dos próximos 7 dias.

## 2. Encontrar ideias: engenharia reversa da demanda (mensal)
- Fontes reais, nesta ordem:
  1. perguntas do WhatsApp (`claude/analise-conversas-whatsapp.md`: "quanto tá o gás?", "faz entrega?", taxa do Gás do Povo, CPF e código);
  2. comentários e DMs do Instagram;
  3. calendário regional;
  4. formatos do concorrente, só como referência.
- Organize em 5 categorias: **PROBLEMAS** (gás acabou, chama fraca), **DESEJOS** (comodidade, domingo aberto), **ERROS** (deixar pra última hora, mangueira vencida), **DESCOBERTAS** (como usar o Gás do Povo, quanto dura um P13) e **OPORTUNIDADES** (datas, comércio, água junto).
- Gere 7 ideias por categoria (35). Para cada uma: tema, manchete (até 40 caracteres), promessa, formato e benefício.
- Dê uma nota de 1 a 5 em atenção, utilidade, facilidade e intenção de pedido. As 10 melhores vão para o topo do `banco-de-pautas.json`.
- Marque o que é demanda comprovada (veio de pergunta real) e o que é hipótese.

## 3. Carrossel: engenharia reversa da promessa
- Comece pelo fim: qual resultado concreto a pessoa tem no último slide? Exemplo: "sabe usar o Gás do Povo", "sabe quando o gás vai acabar".
- Escreva 10 manchetes de capa usando curiosidade, contraste, descoberta e benefício. Escolha as 3 melhores e use a nº 1. Registre as outras 2 no `banco-de-pautas.json`.
- De 3 a 5 slides (limite do nosso formato): capa com promessa forte → uma ideia por slide (`SEM_CTA`, `NUMERO`) → último slide com CTA pro WhatsApp.
- Legenda curta, com CTA de comentário + WhatsApp. Exemplo: "Comente GÁS que a gente te chama". Quem responde é uma pessoa, nunca um robô.
- Revise clareza, ritmo, utilidade e consistência visual. Slide que só enche espaço sai.

## 4. Reel: storyboard de retenção
- 4 momentos: **INTERRUPÇÃO** (0–2 s) → **CURIOSIDADE** → **ENTREGA** (o benefício, sem esconder informação) → **AÇÃO** (CTA pro WhatsApp).
- Escreva 5 ganchos para os 2 primeiros segundos (demonstração, contraste, pergunta específica, informação surpreendente) e use o melhor.
- Divida em cenas com duração, texto na tela, visual e transição. Foto ou vídeo real e rosto humano vêm primeiro.
- Faça 3 versões curtas do roteiro (educativa, demonstrativa e narrativa) e produza a que melhor combina com o material disponível.
- Nunca prometa viralizar. Priorize ritmo e clareza.

## 5. Planejar 7 dias: planejamento por restrições (domingo)
- Restrições:
  - máximo de 2 peças por dia;
  - calendário primeiro;
  - pauta do dia da semana;
  - foto real em pelo menos metade das peças;
  - manchete inédita em 14 dias;
  - capacidade real (sem vídeo novo, nada de reel com rosto).
- Equilibre a semana: **descoberta** (alcançar quem não segue), **educação** (dicas), **autoridade** (revenda autorizada, Gás do Povo, loja física) e **conversão** (CTA direto pro pedido).
- Para cada dia: manchete, objetivo, formato, roteiro curto, CTA, foto ou ilustração e indicador principal (alcance, salvos ou comentários).
- Aponte o que pode ser reaproveitado: um post vira story, um carrossel vira post do Google.
- Horários: use as melhores horas do Metricool como **hipótese de teste**, não como verdade.
- Aprovação: as peças entram no Metricool às 20h34 da véspera, já agendadas. O Gabriel revisa e pode editar ou apagar até a hora de publicar.

## 6. Seguidor → cliente: funil por estados
Jornada da Brasilgás:

**VISUALIZAÇÃO → INTERESSE → COMENTÁRIO ou TOQUE NO LINK → CONVERSA NO WHATSAPP → ORIENTAÇÃO (preço, Gás do Povo, entrega) → PEDIDO → RECOMPRA**

- Para cada estado, defina o objetivo, o gatilho, a mensagem, a ação esperada e a métrica.
- O que pode ser automático: a publicação das peças. O que é sempre humano: a resposta no WhatsApp e nos comentários. Não usar ManyChat nem resposta automática, por regra do Gabriel.
- Teste o funil como um comprador e aponte 5 pontos de abandono. Exemplos: link da bio sem mensagem pronta, demora na resposta nos picos (9h–11h e 16h–17h), preço sem contexto, dúvida sobre a taxa do Gás do Povo.
- Nunca use promessa falsa nem mensagem que fira as regras das plataformas.

## 7. Aumentar alcance e vendas: ciclo de aprendizado contínuo (semanal)
- Dados dos últimos 7 dias:
  - Metricool: publicações, views, alcance, compartilhamentos, salvos e comentários;
  - Gabriel: conversas novas, pedidos e clientes novos.
- **Fase 1.** Indicadores por peça, só com os dados que existem.
- **Fase 2.** Quais temas, ganchos, formatos e CTAs foram melhores que o histórico do perfil.
- **Fase 3.** Onde está o gargalo: alcance, engajamento, conversa ou pedido.
- **Fase 4.** 5 hipóteses de melhoria. Cada uma com a mudança, a métrica principal, o resultado esperado e o critério para avaliar.
- **Fase 5.** 7 ideias novas que usem o que a semana ensinou (vão para o `banco-de-pautas.json`).
- **Entrega.** Resumo curto com as decisões **MANTER / CORRIGIR / REPETIR / INTERROMPER** e o plano dos próximos 7 dias. Cada decisão vira uma linha datada em `aprendizados.md`.
- Não atribua resultado só ao conteúdo. Não invente dados nem prometa crescimento.
