# Brasilgás — produção diária de conteúdo

Repositório usado pela tarefa agendada diária. As artes ficam em `midia/AAAA-MM-DD/` e o Metricool lê pelos links raw públicos.

## Regras de marca (não negociáveis)
- Preço NUNCA aparece em arte nem legenda (preço só no WhatsApp).
- Botijão P13 sempre prata, sem logo. Mascote prata e P13 nunca lado a lado.
- Brasilgás é revenda autorizada; Paragás é a marca do gás.
- Dados fixos: WhatsApp (91) 98222-7035 e 98548-0434; seg–sáb 7h–20h, domingos e feriados 7h–13h; Alameda Padre Rolim, 139, Castanhal.
- Gás do Povo: revenda credenciada (pode citar).
- Nunca inventar promoção, cupom, desconto, prazo de entrega ou preço. Se a pauta pedir oferta e não houver oferta confirmada em `ofertas.json`, troque por outro tema.
- Conteúdo original. O Grupo Leo Gás é só referência de formato.

## Aprendizados (ler TODO dia)
Leia `aprendizados.md` antes de produzir. Ele guarda o que aprendemos com o Gabriel e com os resultados. Quando algo novo for aprendido numa execução (erro, correção, resultado claro), acrescente uma linha datada lá.

## Skill obrigatória
Antes de produzir qualquer peça, leia `skills/brasilgas-conteudo/SKILL.md` (ou use a skill `brasilgas-conteudo`, se estiver listada) e siga o método dela, incluindo a seção 0: usar as skills dos plugins Marketing e Social Media Skills quando estiverem disponíveis.

## Fluxo diário
1. Ler `pauta.json` e escolher o tema do dia da semana (fuso America/Belem). Evitar repetir manchete dos últimos 14 dias (`historico.json`).
2. Escrever o spec (KICKER, HEADLINE, SUB, CTA) e renderizar: `python3 render.py spec.json saida.png feed|story`.
3. Conferir a imagem (ler o PNG) antes de seguir.
4. Commit + push em `midia/AAAA-MM-DD/`.
5. Rodar o VERIFICADOR (seção abaixo) e só então agendar no Metricool (blogId 7861236) no melhor horário do dia, com legenda + CTA + hashtags locais.
6. Atualizar `historico.json`.

## Calendário inteligente (verificar TODO dia, antes da pauta)
- Ler `calendario.json`. Para cada evento, cada janela "D-N:formato" vence na data (evento − N dias). Se vence hoje e `historico.json` ainda não tem `evento` = "<id>:<janela>", produzir essa peça.
- Evento do calendário tem prioridade sobre a pauta do dia. Máximo de 2 rascunhos por dia (1 do calendário + 1 da pauta, ou 2 do calendário).
- tipo "feriado": usar o horário especial 7h–13h (regra da revenda). "ponto_facultativo": não afirmar horário. "cultural"/"comercial": horário normal.
- Story de véspera (D-1) agendar entre 17h e 19h. Story do dia (D0) agendar às 7h.
- Datas regionais têm peso: Círio (maniçoba cozinha por dias, então o gás não pode faltar), Semana Santa, quadra junina, Aniversário de Castanhal (28/01), Adesão do Pará (15/08).
- Em dezembro, completar o calendário do ano seguinte (regras de cálculo em `_manutencao`) e avisar o Gabriel.

## Água (regra do Gabriel, 21/11)
- Divulgar só "Água", "Água 20L", "Galão 20L", "Galão de água 20L" e variações. NUNCA citar marca da água (a marca é informada no atendimento).
- Foto real com rótulo de marca de água legível não pode ser usada (ver fotos/catalogo.json).

## Fotos reais
- `fotos/catalogo.json` lista as fotos da revenda (fachada, estoque de P13, galões) com descrição e uso. Usar só as com "liberada": true.
- Usar no spec: `"FOTO": "fotos/<arquivo>.jpg"` → foto de fundo com véu vermelho (topo e base escuros, meio mostra a foto). Pode combinar com ILUSTRACAO, mas o normal é foto sem ilustração.
- A foto é tratada automaticamente (tratar_foto.py) e a frase (SUB) vai para a base da foto, acima do botão do WhatsApp.
- Usar foto real em pelo menos metade das peças da semana (gente real e loja real engajam mais que desenho).
- Prioridade: fachada com Gás do Povo e letreiro PARAGÁS (confiança, loja física) e pilhas de P13 prata (tem gás).

## Atendimento
- O atendimento no WhatsApp é orgânico (pessoas). O conteúdo só leva a pessoa até lá; nunca prometer resposta automática.

## Ilustrações
- Spec aceita `"ILUSTRACAO": "botijao"` (padrão), `"galao"` (mascote da água 20L) ou `"combo"` (botijão + galão, para gás e água juntos).
- Peça sobre água 20L SEMPRE usa "galao" ou "combo". Nunca só o botijão.

## Carrossel
- Formato "carrossel": de 3 a 5 slides em feed (1080x1350). Os slides do meio usam `"SEM_CTA": true` e `"NUMERO": "2/5"`. O último slide tem CTA. Pode usar `"SEM_BOTIJAO": true` para variar.
- No Metricool é um POST com várias URLs em `media`, na ordem.
- Ideias que funcionam no @souparagas: histórias em sequência ("contos da cozinha sem gás"), comidas típicas por data, homenagens.

## Aprendizados dos prints (19/11/2026)
- LOGO OFICIAL (decidido em 21/11): "BRASIL" azul + "GÁS" vermelho, sobre faixa vermelha "PARAGÁS", numa caixa branca. Nunca usar o logo antigo do Canva (GÁS cinza + ícone azul).
- Mascote prata (botijão com olhos) já é usado pela marca e o público reconhece.
- No Leo Gás, o que mais engaja é atendente real falando pra câmera (com fundo trocado), muito mais que arte feita só com IA. Priorizar rosto humano nos Reels quando houver fotos ou vídeos em `fotos/`.
- Se usar imagem gerada por IA, marcar isAiGenerated:true no Metricool.

## Referência visual @souparagas (confirmado com Gabriel em 19/11/2026)
- Horário confirmado: seg–sáb 7h–20h; domingos e feriados 7h–13h.
- A Brasilgás NÃO atende pelo Zé Delivery e não participa de cupons da Paragás. Nunca citar Zé Delivery, app de terceiros ou cupom da Paragás.
- Do @souparagas usar só a linguagem visual: vermelho com amarelo de destaque, faixa "PARAGÁS", apelido "Pratinha" para o botijão prata, carrosséis com história, comidas típicas por data, homenagens em datas comemorativas.

## Informações nos rascunhos (pedido do Gabriel em 20/11/2026)
- Story continua automático e sem legenda (o Instagram não aceita legenda em story). Mas TODO rascunho, inclusive story, leva `mediaAltText` com a descrição da arte e o texto que aparece nela, para o Gabriel ver no Metricool do que se trata.
- Post, carrossel e reel: legenda completa sempre (gancho, benefício, WhatsApp, horário, endereço, hashtags) + `mediaAltText`.

## Publicação automática com verificador (decidido pelo Gabriel em 21/11/2026)
O Gabriel autorizou a publicação automática, desde que exista o verificador e o relatório diário de resultados.
- Loop de cada peça (executa → checa → melhora → repete):
  1. renderizar com render.py (que gera `<arte>.png.layout.json`);
  2. salvar a legenda em `.txt` e a descrição em `alt.txt`;
  3. `python3 validate.py --formato <f> --spec <spec.json> [--spec ...] --imagem <png> [--imagem ...] --legenda <txt> --alt <alt.txt>`;
  4. se REPROVADO, corrigir o que foi apontado e rodar de novo (no máximo 3 tentativas);
  5. abrir a imagem final com Read e conferir com os próprios olhos (o verificador não vê estética).
- APROVADO → agendar com `draft:false, autoPublish:true` (publica sozinho no horário).
- REPROVADO depois de 3 tentativas → agendar com `draft:true` e avisar o Gabriel no resumo final, dizendo o que falhou.
- Story de feriado/horário e posts do calendário seguem a mesma regra.

## Relatório diário de resultados (todo dia, no início da execução)
- Buscar no Metricool (getAnalyticsDataByMetrics, brandId 7861236) os números do dia anterior:
  IGEV01 seguidores, IGEV43 ganhos, IGEV44 perdidos, IGEV05 visualizações, IGEV06 alcance, IGEV42 contas engajadas,
  IGEV13 curtidas no feed, IGEV14 comentários no feed, IGEV15 salvamentos no feed, IGEV40 compartilhamentos no feed,
  IGEV22 reels, IGEV23 views de reels, IGEV27 curtidas em reels, IGEV28 comentários em reels, IGEV29 salvamentos em reels, IGEV39 compartilhamentos de reels,
  IGEV16 stories, IGEV18 alcance de stories.
- Acrescentar uma linha em `metricas.csv` (data + esses campos; vazio vira 0).
- Por peça publicada nos últimos 7 dias: buscar alcance, curtidas, comentários, salvamentos, compartilhamentos e views
  (posts IGPO*, reels IGRE*, stories IGST*) e atualizar `metricas_posts.csv` (uma linha por peça, sobrescrevendo a anterior).
- No resumo final ao Gabriel, mostrar SÓ o básico: seguidores (e variação), alcance, curtidas, comentários e views de reels de ontem, mais o que foi agendado hoje. Sem análise extra (pedido dele em 21/11: começar simples e aprimorar depois).

## Música nos Reels
- Reel leva música do catálogo do Instagram via `instagramData.audioConfiguration` (só `audioId`; `audioVolume` 100 e `videoVolume` 0 quando o vídeo não tem fala).
- Escolher músicas animadas, populares no Brasil e adequadas a marca familiar (nada com palavrão ou duplo sentido). Ver `musicas.json`.
- Se o Metricool rejeitar por haver vários candidatos, escolher o mais adequado da lista e tentar de novo com o id numérico. Guardar ids que funcionaram em `musicas.json`.
- Se rejeitar por tipo de conta (exige conta Business ligada a uma Página do Facebook), publicar sem música, anotar em `musicas.json` ("audio_bloqueado": true) e avisar o Gabriel uma única vez.

## Google Meu Negócio (decidido pelo Gabriel em 21/11/2026)
- ⏸️ PAUSADO desde 21/11: o perfil do Google ainda está com o nome antigo (Mastergas). NÃO publicar no Google até o Gabriel confirmar que o nome mudou para Brasil Gás. Ele avisa na conversa e esta linha é removida.
- WhatsApp Status fica de fora (nenhuma ferramenta publica lá).
- O Google Business Profile ESTÁ conectado (confirmado em 21/11; o getBrandSettings não lista o Google, mas publicar funciona). TODO post de feed (não story) também vai para o Google:
  - mesmo createScheduledPost, com providers [{"network":"instagram"},{"network":"gmb"}] e "gmbData": {"type":"publication"};
  - o texto do Google é o mesmo da legenda, mas sem hashtags e sem emojis em excesso (o Google não usa hashtag); se precisar, criar um post separado só para gmb com texto adaptado (até 1500 caracteres);
  - incluir sempre: o que vende (gás P13 Paragás, água 20L), "Castanhal", entrega, Gás do Povo quando fizer sentido, WhatsApp e horário. Isso ajuda a aparecer em buscas como "gás perto de mim" e "entrega de gás Castanhal".
- Se o Metricool recusar o post no Google, publicar só no Instagram e avisar o Gabriel no resumo.

## Destaques (manual, o Metricool não alimenta)
- Destaques do perfil: Gás do Povo, Entrega, Água 20L, Onde fica, Horário (e Clientes, quando houver depoimentos).
- Quando o story do dia combinar com um destaque, incluir no resumo uma linha: "📌 Story de hoje (HHh) cabe no destaque <nome>: abra o story e toque em Destacar."
