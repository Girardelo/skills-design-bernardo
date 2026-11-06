---
title: "Criar telas"
company: global
classification: internal
verified_at: 2026-10-31
status: em uso
index: true
---

# Criar telas

Como criar ou refazer telas de sistema, app, portal e painel. Enxugado em 25/10/2026 a pedido de Bernardo ("to pedindo para serem criadas interfaces e n to gostando do que ta sendo apresentado utilizando o brain"): o texto antigo tinha 195 linhas de regras sobre conduzir o trabalho e quase nada sobre o que ele acha bonito. Texto anterior completo em [[Projetos/Histórico/INTERFACES-até-2026-10-24|histórico]]. Executa pela skill `design-de-sistemas`. Landing page e site seguem [[Capacidades/Processos/Criação-de-sites-por-etapas|sites e LPs por blocos]].

**Entrada desde 31/10/2026:** [[Capacidades/Processos/Padrão-de-tela-e-página|Padrão de tela e página]], com o caminho, os parâmetros do nível Virapátio, a régua de 8 perguntas antes de mostrar e a regra de variação. Esta nota guarda o que é só de tela de sistema: o que decide se a tela fica boa, os passos na tela e a régua por produto.

## O que decide se a tela fica boa

1. **Gosto de Bernardo, por imagem.** Antes de propor, abrir [[Conhecimento/Referências-de-interface|Referências de interface]] (telas reais que ele aprovou ou recusou) e citar, em cada opção, de qual referência veio cada decisão visível. Ver também [[Conhecimento/Interfaces-sem-cara-de-IA|Interfaces sem cara de IA]] (29/10/2026): 15 regras para conferir a tela antes de mostrar, com a origem de cada uma nos dois vídeos e os conflitos com as escolhas do Gira. Nunca repetir o que está em "Não fazer". Se não houver referência aprovada do tipo de tela, buscar 3 a 5 telas reais de produtos de primeira linha (vistas na tela, não descritas) e mostrar junto.
2. **A cara real do sistema.** Opção sai com a casca, as cores, as letras e os dados reais do produto, renderizada em alta resolução, nos dois temas. Caixa genérica, mapa desenhado ou dado inventado foi "ridiculamente ruim" (16/10, MF Cargas).
3. **Hierarquia antes de enfeite.** "Além de funcional e simples, tem que ser esteticamente agradável e manter hierarquia visual; isso é o básico" (16/10). Funcionar e passar nos testes não basta.
4. **Nada com cara de IA.** Sem caixas e etiquetas genéricas, letra pequena, brilho, pílula, fundo creme, rótulo numerado ou em fonte mono (lista da casa). Conferência testável por item, com a origem nos dois vídeos de 29/10/2026: [[Conhecimento/Interfaces-sem-cara-de-IA|Interfaces sem cara de IA]]. Cor, brilho, pílula, fonte mono e imagem 3D só mudam com decisão do Gira; a lista acima continua valendo. Teste final: a sessão só mostra a opção se a colocaria com orgulho ao lado das referências (21/10, radar do Virapátio).
5. **Pensada para o dia a dia.** Busca e filtro quando a lista cresce, valor já preenchido, atalho para a ação mais comum, poucos toques, vazio que ensina (13/10). Carregar, erro, vazio e espera com o mesmo cuidado das telas principais, sem piscar nem texto técnico (15/10).

## Como fazer (uma tela por vez)

"Pode demorar um pouco mais, mas a entrega com certeza vai ser melhor" (13/10): todas as telas de uma vez saem genéricas. O caminho é o do [[Capacidades/Processos/Padrão-de-tela-e-página#O caminho|padrão]]; na tela de sistema, ele fica assim:

1. **Entender** em duas linhas: quem usa, onde (celular ou computador), qual tarefa resolve. Ler a nota do projeto e o que já foi escolhido, para não reabrir, e abrir a última versão aprovada da tela ou do produto: ela é o piso.
2. **Referências:** as aprovadas do mesmo tipo (item 1 acima) e a régua do produto, se existir.
3. **3 opções** da tela (2 quando a escolha é só de fluxo ou texto), comparáveis, com a recomendação e o motivo em uma linha cada. Antes de mostrar, cada opção passa pelos critérios de tela (`design-de-sistemas/references/criterios-de-tela.md`: cena de uso, tarefa antes dos campos, escolher em vez de digitar, até ~5 toques, uma ação principal, onde estou, volume real); o que não tirar 2 é corrigido antes, e a opção só vai se responder sim às 8 perguntas da régua do padrão.
4. **Bernardo escolhe** (opções em letras, refino numerado: A1, C3). A escolha vira linha nas Referências de interface ou na régua do produto, com data.
5. **Aplicar e conferir** no computador e no celular; mandar as fotos. Só então a próxima tela.
6. **Animação** entra no fim, numa passada única.

Ajuste pequeno (tela que já existe, sem fluxo novo nem escolha visual nova) não passa pelas opções: corrige, confere pela régua e manda as fotos (22 e 24/10). Tela nova, fluxo novo ou escolha visual nova seguem os passos acima.

## Régua por produto

Em teste desde 24/10/2026 no Virapátio ("vamos para testar"): cada produto ganha uma régua escrita com o que Bernardo aprovou ou recusou (`docs/REGUA-DA-TELA.md`) e uma conferência automática no computador e no celular (`scripts/regua-da-tela.cjs`). Direção de tela nova é dele; ajuste em tela aprovada a sessão confere pela régua, grava e manda as fotos depois. Se der certo, levar para os outros produtos. A régua do produto é o detalhe dos itens 5 e 8 da régua do padrão.

## Quando houver ajudantes

Só com pedido de Bernardo ou ultracode ligado. Rodada em lote por agentes saiu "um lixo" (21/10): o agente não lê o Brain sozinho. O pedido leva, por caminho absoluto: `../../contexto/padrao-de-tela-e-pagina.md`, esta nota, `../../contexto/referencias-de-interface.md` com as imagens, os critérios de tela, a nota do projeto e o handoff mais recente, a tela atual e o critério de pronto. O agente devolve opções; a sessão principal confere pelo item 4 antes de mostrar qualquer coisa. Sessão separada por tela só quando Bernardo pedir com essas palavras (19/10).

## Fixos

- Sem Figma (29/09); telas por imagem, referência, prévia local e código.
- Projeto da casa: referência no X pelo Grok Bot antes de peça visual (regra da casa, 20/10).
- Escolha registrada: casa no Painel KZA e na nota do projeto; cliente na nota do projeto.
- O [[Conhecimento/Repertório-UI-UX-do-GitHub|repertório do GitHub]] é apoio para nomear estilos, não referência visual: nunca substitui as imagens.

[[CAPACIDADES|Capacidades]] · [[CONTINUIDADE|Continuidade]] · [[INICIO|Início]]
