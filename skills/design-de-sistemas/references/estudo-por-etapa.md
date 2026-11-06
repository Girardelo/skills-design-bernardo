# Estudo aplicado antes das propostas visuais

Usar ao iniciar uma nova parte da interface ou quando uma dúvida alterar seus fundamentos. Esta referência orienta o que investigar; não significa que cada tópico já foi pesquisado para o produto atual. Escolher apenas as linhas pertinentes e consultar a documentação necessária antes de atribuir recomendações a uma fonte.

## Converter pesquisa em uma proposta que possa ser avaliada

Recuperar objetivo, pessoas/tarefa, decisões vigentes, tela representativa e restrições. Estudar o ponto aberto em fontes primárias, confrontar com o contexto e explicar a consequência prática. Uma norma pode estabelecer um requisito; a solução adotada por um sistema de design é uma referência; a composição recomendada para o produto é uma decisão a justificar. Não apresentar essas três coisas como se fossem a mesma autoridade.

Uma apresentação curta pode seguir: **o que esta parte precisa resolver → princípio e fonte → aplicação ao produto → diferenças entre opções → recomendação e motivo → verificação na implementação**. Não usar esse formato como formulário obrigatório nem exigir um documento por microajuste.

As imagens devem demonstrar os critérios. Se o estudo aponta prioridade entre ações, mostrá-la na tela; se trata de leitura, incluir conteúdo realista; se trata de tema escuro, mostrar relações entre fundo, superfícies, texto e estados. Não gerar apenas amostras decorativas desconectadas do uso.

## Perguntas por parte da interface

| Parte | O que estudar e decidir | O que mostrar e conferir |
| --- | --- | --- |
| Fundo e superfícies | Papel do canvas, agrupamento e camadas; distração e relação com áreas de leitura | Conteúdo sobre o fundo e painéis sobrepostos; legibilidade nos temas em escopo. Conforto prolongado permanece hipótese até avaliação em uso |
| Tipografia | Hierarquia, leitura contínua, comprimento de linha, pesos, tamanho e entrelinha | Títulos, corpo, apoio e dados densos; texto longo e ampliação. Não presumir que uma família de fonte comprova acessibilidade |
| Cores e temas | Papéis semânticos, ênfase, interação, seleção, foco, estados e relações de contraste | Mesma função nos temas claro/escuro, pares de cor medidos, rótulos/ícones além da cor; estados dos controles |
| Espaçamento e densidade | Proximidade, agrupamento, ritmo e espaço necessário para operar | Mesma tela com conteúdo realista; distinguir grupos sem desperdiçar área útil ou dificultar alvos de interação |
| Bordas e sombras | Separação decorativa, identificação de controles, elevação e sobreposição | Painéis, campos, menus e diálogos nos temas pertinentes; distinguir contorno funcional de decoração, sem exigir contraste universal de toda borda |
| Menu lateral e superior | Arquitetura da informação, orientação, frequência de acesso, indicação de localização | Itens, seleção, recolhimento e overflow; teclado e estados ativo/foco; coerência entre variantes autorizadas |
| Cabeçalho e retorno | Identidade da página, contexto, ações e destino de retorno | Títulos longos, ações e retorno reconhecível; testar preservação de filtros, seleção e rascunhos na implementação |
| Personalização da aparência | Opções compreensíveis, prévia e alcance da preferência | Claro/escuro, preferência do sistema e variantes existentes quando em escopo; verificar persistência, primeiro carregamento e continuidade de navegação |
| Estrutura em diferentes larguras | Prioridade e reorganização do conteúdo, limites intrínsecos, overflow e reflow | Larguras representativas e pontos em que a composição muda; testar expansão de texto e controles sem corte. Imagens não comprovam responsividade |
| Ação | Prioridade por contexto, rótulos, ação/navegação, consequência e recuperação | Ação principal, secundária e destrutiva quando pertinente; hover, pressionado, foco, indisponível e carregando; feedback e proteção contra repetição indevida |
| Campos | Tipo de entrada, rótulo, ajuda, formatos, obrigatoriedade e validação | Vazio, preenchido, erro e estados pertinentes; teclado, mensagens úteis, texto longo e preservação dos valores |
| Organização | Agrupamento, comparação, leitura, densidade e volume | Lista/tabela/cards conforme a tarefa; vazio, muitos itens, nomes longos e ações relacionadas; não impor o mesmo recipiente a todas as tarefas |
| Navegação | Destinos, contexto, localização, descoberta e continuidade | Abas, breadcrumbs, paginação ou etapas conforme o problema; diferenciar navegação de ação e verificar retorno/teclado |
| Feedback | Tipo de resultado, duração, urgência, recuperação e anúncio acessível | Sucesso, informação, atenção, erro, vazio e carregamento pertinentes; mensagem com próximo passo e resultado verdadeiro, sem depender apenas de cor |

## Pesquisa de cor: exemplo do nível de fundamentação

- Definir funções antes de escolher valores: fundo, superfícies, texto, apoio, ação, seleção, foco e estados. Tokens podem manter a mesma função com valores diferentes entre temas. Referências: [Atlassian Color](https://atlassian.design/foundations/color) e [Carbon Color](https://carbondesignsystem.com/elements/color/overview/).
- Dar ênfase de acordo com a prioridade no contexto. A recomendação de destacar a ação principal não deve virar uma regra de um único botão em todo o aplicativo. Consultar [Atlassian Button usage](https://atlassian.design/components/button/usage) e relacionar a orientação à tarefa da área.
- Conferir os pares efetivos de texto e fundo. A WCAG AA estabelece 4,5:1 para texto comum e 3:1 para texto grande nas condições definidas pelo critério; há exceções. Não arredondar um valor abaixo do limite para declarar aprovação. Fonte: [Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- Identificar os sinais visuais necessários para reconhecer controles e estados e avaliar seu contraste com as cores adjacentes pertinentes. O requisito de 3:1 não se aplica automaticamente a toda borda decorativa. Fonte: [Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
- Expressar informação e estados com alternativa visível à cor e prever foco de teclado reconhecível. Referências: [Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) e [Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html).

Essas fontes foram consultadas na etapa de cores em 19/09/2026. São pontos de partida; conferir os trechos e versões pertinentes quando uma nova decisão depender deles. Não transportar a paleta de um projeto nem tratar este conjunto como cobertura de todas as exigências de acessibilidade.

## Da imagem à validação

Manter conteúdo e composição comparáveis enquanto a dimensão escolhida varia. Incluir apenas estados e exemplos suficientes para avaliar a decisão; não transformar toda prancha em uma biblioteca completa. Na apresentação, indicar a opção recomendada e o motivo, sem substituir a escolha do usuário quando ela fizer parte do processo combinado.

Antes de entregar, inspecionar a imagem e conferir correspondência com os critérios. Textos, medidas e cores de uma geração podem divergir do solicitado: indicar a especificação pretendida separadamente quando necessário e corrigir desvios relevantes. Não usar a imagem como prova de contraste medido, fonte exata, teclado, persistência ou responsividade.

Após a escolha, traduzir a etapa para componentes/tokens no projeto autorizado e testar o alcance atingido. Recuperar o estudo válido nos refinamentos. Registrar decisão, fonte e pendência no contexto existente, mantendo as escolhas de cada projeto em seu perfil e os critérios transferíveis nesta skill.
