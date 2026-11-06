# Layout, componentes e acabamento

Use o trecho pertinente à decisão. Valores aprovados vêm do projeto; esta referência não define uma estética universal.

## Escolher a composição

| Tarefa dominante | Composição a considerar | Verificação que decide |
| --- | --- | --- |
| Comparar muitos registros por atributos | Tabela ou lista estruturada | Consegue comparar sem abrir cada item? |
| Reconhecer e escolher imagens | Galeria ou carrossel com controles | Consegue alcançar e distinguir todas as opções? |
| Ajustar algo e ver o resultado | Painel integrado de edição e prévia | Controles e resultado permanecem relacionados e legíveis? |
| Inspecionar itens em sequência | Lista com detalhe contextual | Trocar de item preserva contexto e deixa clara a seleção? |
| Organizar horários | Agenda com vista adequada ao volume | Data, hora, conflito e ação ficam identificáveis? |
| Executar duas tarefas principais distintas | Seções ou entradas com prioridades claras | A escolha orienta ou apenas acrescenta um clique? |

Uma tabela pode reunir busca, ordenação, ações individuais e em lote; a documentação do [Carbon Data Table](https://carbondesignsystem.com/components/data-table/usage/) oferece esse repertório. Não exige copiar o estilo Carbon nem usar uma tabela em qualquer coleção.

## Proporção e densidade

Compare a página no **mesmo viewport** da referência. “Muito larga”, “esticada” e “fora do padrão” podem apontar para largura, altura, escala, distribuição ou zoom. Observe esses aspectos antes de reduzir o contêiner.

- Derive a área útil do shell e suas margens. Um frame de 1440px não oferece 1440px para o conteúdo quando existe menu lateral.
- Use largura compatível com a informação: um título curto editável não precisa atravessar a página; uma tabela comparativa pode precisar desse espaço.
- Agrupe texto, ação e contexto por proximidade. Um aviso pequeno com botão distante parece pertencer a outra tarefa.
- Ajuste densidade pelo uso: elementos de comparação próximos, respiro entre grupos, área suficiente para tocar/clicar. Não comprima texto até ficar ilegível para “caber tudo”.
- Rolagem é legítima quando o conteúdo exige. Não fixe a altura do conteúdo no viewport, esconda overflow útil ou crie várias rolagens internas só para reproduzir uma captura.
- Centralização real usa o centro da região definida. Controles laterais com larguras diferentes podem deslocar um título mesmo dentro de um flex centralizado; use colunas simétricas ou estrutura equivalente e teste colisões.

## Hierarquia e identidade

Defina a primeira leitura: propósito da página, objeto/contexto necessário, área principal de trabalho e próxima ação. Título curto e funcional; subtítulo apenas se acrescentar informação. Evite repetir a mesma orientação no breadcrumb, título, subtítulo e card.

Reutilize tokens, escala de texto, raio, bordas, família de ícones e padrão de imagem. Expresse identidade por uma composição reconhecível e pelo acabamento desses elementos. Não adicione hero de marketing, gráfico sem dado, KPI fictício, gradiente ou movimento para preencher espaço. Uma referência externa contribui com um princípio visual; o padrão do produto e a tarefa determinam sua adaptação.

Em pedido criativo, compare hipóteses espaciais de verdade: edição e prévia no mesmo painel, prévia central com controles laterais ou faixa compacta de ferramentas, por exemplo. Escolha com base na área útil e na tarefa; a solução menos chamativa não é automaticamente a melhor.

## Anatomia e contratos dos componentes

| Componente | Resolver na interface | Conferir no uso |
| --- | --- | --- |
| Botão/ação | Verbo claro, hierarquia e alcance; ícone quando esclarece | Estado de foco, clique repetido, ação executada e feedback |
| Link de retorno | Destino contextual e aparência reconhecível | Volta ao objeto/caminho certo com dados preservados |
| Campo | Rótulo persistente, formato, largura e ajuda necessários | Valor longo, erro, dado ausente, digitação e correção |
| Busca | O que encontra, como limpar e onde mostra resultados | Busca real no escopo prometido, ausência de resultado e seleção |
| Card | Identidade, informação para decidir, ação e estado | Conteúdo variável; não confundir clique no corpo, controle interno e arrasto |
| Barra de etapas | Ordem, etapa atual e conclusão/pendência | Voltar não apaga edição; ícone tem significado acessível |
| Fila/seleção | Quantidade, item atual e ação sobre o conjunto | Remover/filtrar/navegar não troca identidades |
| Feedback | Resultado real e orientação para continuar | Erro não limpa dados; sucesso não antecipa confirmação |

Não transforme todo texto em botão; diferencie ação, navegação e informação. Uma ação prioritária por contexto costuma simplificar a leitura, mas ações repetidas em cards independentes podem ser legítimas. Evite dois botões fortes competindo pela mesma decisão. Ações indisponíveis precisam de motivo encontrável quando não for evidente; não use tooltip inacessível como única explicação.

Na implementação, seleções e estados pertencem a identificadores estáveis, não à posição do item na lista. Componentes compartilhados devem expor variantes necessárias, sem um único componente cheio de exceções por página. Estenda a biblioteca quando houver repetição real; não construa um design system inteiro antes de entregar uma aba.

## Carrossel para seleção

Defina quantidade visível, proporção de imagem, avanço e recorte. Um trecho do próximo item pode revelar continuidade, mas não substitui controles compreensíveis.

- Ofereça anterior/próximo com nomes acessíveis e comportamento coerente no início/fim. Não esconda permanentemente itens ou ações fora do alcance de teclado.
- Separar deslocamento de escolha: um gesto para navegar não pode adicionar à fila nem escolher uma foto por acidente.
- Conteúdo de seleção fica parado por padrão. Autoplay exige uma finalidade explícita e controle de pausa; não herde movimento de um hero decorativo.
- Com um item, controles de avanço não devem prometer opções inexistentes; com muitos, todos precisam ser alcançáveis e o carregamento deve ser compatível com o volume.
- Preserve a identidade e a seleção durante filtragem, carregamento ou reordenação. Se uma seleção deixa de estar visível, torne o estado compreensível.

O [padrão Carousel do W3C APG](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/) orienta controles, foco e rotação; um trilho com overflow nativo não exige aplicar todos os papéis ARIA de um slideshow. O [critério sobre arrasto](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) pede alternativa por clique/toque para operações de arrastar implementadas pelo conteúdo, ressalvadas suas exceções. Só adicionar suporte a teclado não substitui essa alternativa. A rolagem nativa do navegador é tratada de forma diferente; não invente uma violação sem inspecionar a implementação.

## Acabamento que sobrevive ao uso

Conferir textos reais/longos, imagens com enquadramentos diferentes, dados ausentes, estados de foco e ausência de imagem. Preservar proporção e decidir conscientemente entre conter e recortar; não esticar foto ou logo.

Se houver movimento, use-o para indicar relação ou mudança de estado. Não mover controles enquanto a pessoa tenta agir; considerar preferência de movimento reduzido na implementação. Se o fundo precisar ser sutil, avaliar junto do texto e dos cards, não apenas em um recorte vazio.

Acessibilidade deve ser observada no componente: nome, função, estado, operação e foco. Não use só cor para seleção, erro ou conclusão. Um ícone de check pode manter o visual curto, com descrição de etapa concluída disponível à tecnologia assistiva. Verificar contraste nos pares reais de cor; nenhum “azul da marca” é automaticamente adequado para todo texto.

Fontes externas acima consultadas em 15/09/2026. São referências de comportamento; os critérios de composição e sua adaptação ao trabalho de Bernardo são síntese de projeto.
