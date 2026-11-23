# Aprendizados da Brasilgás (loop de evolução)

Cada linha: data · o que aprendemos · o que mudou no sistema. Lido pela tarefa diária e nas conversas com o Gabriel.
Quando uma regra daqui virar permanente, ela sobe para CLAUDE.md ou para a skill.

## Sobre o Gabriel e o jeito de trabalhar
- 19/11 · Prefere opções a perguntas abertas; tom casual; quer o sistema funcionando sozinho, mas com controle.
- 21/11 · Relatório: começar simples (números básicos) e aprimorar depois. "Peça campeã" ficou exagerado → removido.
- 21/11 · Quer evolução constante, não só testes: o que aprendemos nas conversas deve virar regra aplicada → criado este arquivo.
- 21/11 · Preza por economia e sofisticação: menos ferramentas, bem escolhidas.

## Marca e negócio
- 19/11 · Preço só no WhatsApp (houve post antigo com R$ 117,99; não repetir).
- 19/11 · Horário: seg–sáb 7h–20h; domingos e feriados 7h–13h (confirmado).
- 19/11 · Não atende pelo Zé Delivery; Paragás é só referência visual.
- 21/11 · Norte do projeto: perfil otimizado + anúncios pagos levando ao WhatsApp.

## Conteúdo e Instagram
- 19/11 · No Leo Gás, atendente real falando pra câmera engaja de 2 a 3 vezes mais que arte só de IA.
- 20/11 · Story não tem legenda no Instagram; a informação vai na arte e no texto alternativo.
- 20/11 · Rascunhos não aprovados não saem (stories do feriado se perderam) → publicação automática com verificador a partir de 21/11.
- 21/11 · Instagram limita a 5 hashtags por post desde dez/2025 (soube pela skill hashtag-strategy, confirmado) → verificador agora exige de 3 a 5.
- 21/11 · As artes v1 estão simples demais (só texto e botijão desenhado). Falta imagem real (fotos, logo, mascote) e uma ferramenta de design.

- 21/11 · Métricas do dia anterior às 5h30: seguidores e alcance ainda vêm 0 (Metricool atualiza com atraso); stories antigos não aparecem em IGST. No relatório, usar o último seguidor não-zero e marcar como "ainda não atualizado".

- 21/11 · Água 20L ainda é fase experimental: vende, mas não era divulgada por falta de identidade. Gabriel pediu um mascote/sticker do galão → criado o mascote galão azul sorridente (templates/ilustracoes/galao.svg) e o combo botijão + galão. Peças de água usam "ILUSTRACAO": "galao" ou "combo".

- 21/11 · Layout v1.1 a pedido do Gabriel: texto centralizado e distribuído (antes ficava espremido no topo), mascotes alinhados pela base, rodapé com os dias por extenso ("Segunda a sábado, das 7h às 20h · Domingos e feriados, das 7h às 13h"). O template passou a usar layout em coluna (flex), que se ajusta sozinho e evita sobreposição.
- 21/11 · Gabriel: "estou começando a gostar desta nossa marca" → manter esta linha visual (vermelho, logo em caixa branca, faixa amarela, título Anton centralizado, mascotes).

- 21/11 · LOGO OFICIAL decidido: o do Instagram/placa (BRASIL azul + GÁS vermelho + faixa vermelha PARAGÁS, em caixa branca). O logo antigo do Canva (GÁS cinza + ícone azul do botijão) fica aposentado. O template já reproduz o oficial em texto; falta só o arquivo em alta.
- 21/11 · Canva conectado, plano grátis: exporta PNG/JPG, mas não com fundo transparente. O ambiente da tarefa não baixa arquivos do Canva (rede bloqueada); para usar arte do Canva, passar o link de exportação direto ao Metricool.

- 21/11 · Água: divulgar só "Água / Galão 20L", nunca a marca (informada no atendimento) → regra no CLAUDE.md, na skill e no verificador.
- 21/11 · Chegaram 16 fotos reais (fachada com Gás do Povo, letreiro PARAGÁS, estoque de P13, galões) → fotos/catalogo.json. Fotos de galão com rótulo legível ficam bloqueadas.

- 21/11 · De 5 peças dos primeiros dias, 2 se perderam por ficarem como rascunho sem aprovação. Desde 21/11 o que passa no verificador sai sozinho. Primeiras peças com foto real agendadas (post 12h e story 18h).

- 21/11 · Layout v1.2 a pedido do Gabriel: mais respiro entre título e topo (acento encostava), frase desce para a base da foto, botão do WhatsApp maior e centralizado. Fotos passam por tratamento leve automático (tratar_foto.py: contraste, cor, nitidez, vinheta), "mais bonitas sem exagero".
- 21/11 · Logo em texto do template é o LOGO OFICIAL (aprovado pelo Gabriel).
- 21/11 · Atendimento no WhatsApp é orgânico (feito por pessoas, respostas prontas já existem): não automatizar atendimento.
- 21/11 · Link do WhatsApp já está no perfil. Feitos: bio (3 opções), 6 capas de destaque, 5 stories de destaque e 6 peças de anúncio (pasta perfil/ e anuncios/).

- 21/11 · Perfil todo atualizado pelo Gabriel: usuário agora é @brasilgas_caicara, nome "Brasilgás | Gás e Água em Castanhal", bio nova, categoria, endereço, destaques e foto de perfil com o logo oficial (opção A). Primeira publicação 100% automática: story da água às 10h.
- 21/11 · Próxima etapa decidida: anúncios pagos a partir de segunda (23/11).

- 21/11 · Metricool não publica no Status do WhatsApp (nenhuma ferramenta publica). Foco no Google Meu Negócio, que a Brasilgás já tem: posts de feed também vão para o Google quando a conexão existir.

- 21/11 · Endereço oficial: Alameda Padre Rolim, 139, Castanhal (Gabriel confirmou; o Instagram mostrava 138). Atualizado no template, regras, skill e verificador. Google Meu Negócio conectado ao Metricool pelo Gabriel.

- 21/11 · Destaques não podem ser alimentados por ferramenta (limite da Meta). O resumo diário avisa quando o story do dia cabe num destaque. O getBrandSettings não lista o Google, mas o post no Google foi aceito.

- 21/11 · O perfil do Google Maps ainda está como "Mastergas" (bandeira antiga). Posts no Google pausados até a troca de nome. Guia de atualização em perfil/google.md.

- 21/11 · Gabriel criou perfil novo no Google (Brasil Gás) em vez de renomear o Mastergas (estava desativado). Perfil novo precisa de verificação do Google antes de aceitar posts; antigo deve ficar como "Fechado permanentemente" para não duplicar.

- 21/11 · Perfil novo do Google "Brasilgás" verificado (selo azul). Posts no Google religados; primeiro às 12h15.

- 21/11 · Conferido às 12h20: post do Instagram das 12h PUBLICADO (primeiro após trocar o usuário para @brasilgas_caicara, a conexão continuou funcionando) e primeiro post no Google (perfil Brasilgás) PUBLICADO às 12h15.

## Números de referência
- 21/11 · Painel do Instagram: 830 visualizações nos últimos 30 dias, 69 seguidores, 23 posts.
- 21/11 · 68 seguidores. Reel "Sextou" (20/11): 19 views e 2 curtidas.

- 22/11 · Manchete de story que quebra deixando uma palavra sozinha ("13H") fica feia, e o verificador não pega → manchete curta (até ~15 caracteres) para caber em 1 linha, ou conferir a quebra no Read.

- 23/11 · Gabriel trouxe 7 prompts de crescimento (@gurudoprompt) → viraram métodos fixos em skills/brasilgas-conteudo/prompts-crescimento.md (auditoria mensal, banco de pautas, carrossel, reel, plano de 7 dias aos domingos, funil, ciclo semanal MANTER/CORRIGIR/REPETIR/INTERROMPER). Criado banco-de-pautas.json com ideias tiradas das perguntas reais do WhatsApp.
- 23/11 · Gabriel quer ver as peças na véspera: a tarefa diária passou para 20h34 e produz as peças de AMANHÃ, já agendadas (publicam sozinhas; ele revisa à noite e pode editar ou apagar). Escolheu essa opção em vez de rascunho, que se perde quando não é aprovado.
- 23/11 · Foto estoque-p13-pilha-1 em close mostra botijões gastos/enferrujados → evitar como foto principal (anotado no catálogo).
- 23/11 · Fachadas deitadas e de longe (esquina, laterais, contraluz) perdem o letreiro PARAGÁS no recorte vertical e viram "muro vermelho" (story de 22/11 e post de 23/11) → bloqueadas para post e story, reservadas para o Motion Reel. Anúncio e destaque da loja trocados para a foto da frente (Gás do Povo). O post de 23/11 foi refeito com essa foto antes de publicar. Fotos novas: em pé, com o letreiro ou o produto no centro.
- 23/11 · Criado o Motion Reel (motion_reel.py + skills/motion-reel): Reel vertical feito de fotos com pan e zoom até o letreiro. Fusão só das fotos, com o texto trocando no meio da fusão, porque a fusão das camadas de texto deixava letra fantasma. Primeiro Motion Reel: "A loja vermelha da esquina", terça, 24/11.
- 23/11 · Música em Reel: o catálogo de áudio do Instagram deu 403 no Metricool (conta não é Business ligada a uma Página do Facebook) → audio_bloqueado=true em musicas.json; os Reels saem sem música até ligar o Meta Business.
- 23/11 · Gabriel vetou o gancho "A loja vermelha da esquina": não diz que é revenda de gás e parece outro comércio. Regra: o gancho (1ª cena / 1ª linha) tem que dizer GÁS logo de cara (ex.: "O gás acabou? A gente leva"). Fachada entra como prova, depois do gancho de produto. Reel de 24/11 refeito com abertura no estoque de P13.
- 23/11 · Vocabulário (Gabriel): não chamar só de "gás" nem de "botijão 13kg GLP"; usar "recarga", "recarga de gás", "sua recarga". O gancho continua dizendo gás ("Acabou o gás? A gente leva sua recarga").
- 23/11 · Reel de 24/11 refeito com o plugin Motion Reel (fonte em motion-reel-plugin/gas24/): 15 s, 128 bpm, trilha house sintetizada e efeitos no tempo da batida, embutidos no vídeo. Isso contorna o bloqueio de música do Metricool. Textos sempre fora da faixa inferior (≈430 px) que a legenda do Instagram cobre, e nunca em cima do letreiro ou do banner que a câmera mostra.
- 23/11 · Narração com voz da Luzia (ElevenLabs) fica para depois: o Gabriel gera o áudio e o Reel é sincronizado com a fala.
- 2026-11-23: Reel Motion de 15 s ficou corrido (Gabriel): blocos de 2,8 s com 3 linhas são rápidos demais. Padrão agora: ~22 s, cada bloco ≥ 4 s, texto entrando junto com a foto. Na troca deslizante (whip), recortar cada cena no próprio quadro (clip), senão a foto larga aparece crua sem véu. Nunca abrir cena com a câmera passando pelo muro vermelho sem texto.
- 2026-11-23 (20h34): Metricool devolveu TUDO zerado nas métricas (inclusive dias que antes tinham dados, ex.: 21/11 com 3 curtidas) e o getBrandSettings só lista o Google em networksData; a publicação no Instagram segue funcionando (post de 23/11 publicado). Tratado como falha de leitura, não como queda real: linha de 22/11 gravada com 0 e marcada como "sem dado" no resumo. Se repetir, pedir ao Gabriel para reconectar o Instagram nas análises do Metricool.
