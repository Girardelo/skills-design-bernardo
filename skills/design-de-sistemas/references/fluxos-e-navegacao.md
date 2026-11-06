# Fluxos e navegação

Leia para criar uma área, alterar percursos ou antecipar estados. Se o contexto já resolve uma decisão, não a reabra. Estas são heurísticas de projeto; regras do produto vêm de fontes atuais.

## Unidade de trabalho

Comece pelo objeto e pelo resultado, não pelo menu. “Anúncios” pode significar gerenciar peças, campanhas, publicações ou solicitações; esses objetos não são equivalentes. Recupere o escopo existente antes de desenhar um gerenciador completo de mídia paga.

Use uma frase: “A pessoa precisa [ação] sobre [objeto] e reconhecer [resultado]”. Relacione cada bloco importante da tela a localizar, decidir, executar ou acompanhar. Conteúdo que não ajuda uma dessas tarefas precisa justificar seu espaço.

## Navegação em camadas

| Necessidade | Tratamento possível | Armadilha a evitar |
| --- | --- | --- |
| Mudar de área do sistema | Navegação global existente | Criar outro menu global dentro da página |
| Alternar vistas do mesmo contexto | Abas ou controles de vista, conforme implementação | Repetir os mesmos destinos em abas, cards e cabeçalho sem razão |
| Encontrar um registro | Busca, filtros e ordenação junto à coleção | Busca que só filtra a página carregada, anunciada como busca global |
| Inspecionar sem perder a lista | Painel lateral ou detalhe contextual | Abrir uma página zerando filtros e seleção |
| Editar conteúdo extenso ou abrir por link | Página de detalhe com contexto e retorno | Modal comprido com rolagens concorrentes e sem URL útil |
| Executar ação breve que exige foco | Diálogo, quando necessário | Confirmação para toda ação pequena e reversível |
| Concluir passos dependentes | Etapas com progresso e revisão proporcional | Wizard que divide artificialmente um formulário simples |

“Aba” no pedido pode significar uma área da navegação global, não necessariamente um componente ARIA tab. Defina o comportamento antes da semântica. No código, navegação usa links/rotas; ações usam botões; abas internas seguem seu padrão de teclado quando de fato forem abas.

## Continuidade é parte da função

Verifique o retorno exato: de qual registro a pessoa veio? Ao voltar, filtros, busca, ordenação, item atual e escolhas ainda fazem sentido? Defina o tratamento de alterações não salvas conforme o produto; não exiba diálogo de descarte se nada mudou.

Em um fluxo com etapas, diferencie **etapa atual**, **concluída**, **com pendência** e **futura** quando essas situações existirem. Não marque como concluído apenas porque a pessoa passou pela tela. Se editar uma informação invalida outra, atualize o estado correspondente. O visual pode usar ícone; o significado precisa continuar disponível no código acessível.

## Coleções: o exemplo não define a capacidade

Antes de escolher layout, descubra:

- Quantidade esperada e limite real, se houver. Três fotos de demonstração não significam máximo de três.
- Ordenação: campo, direção e desempate estável; não inferir data pelo código ou posição do array.
- Busca/filtro: escopo, limpeza, ausência de resultado e manutenção da seleção.
- Seleção única ou múltipla; adicionar novamente duplica, substitui ou não faz nada?
- Carregamento de mais itens: paginação, busca no servidor ou outra estratégia existente. Não carregue milhares de imagens para sustentar um carrossel demonstrativo.

Casos mínimos para raciocinar: **0**, **1**, **alguns** e **muitos**; seleção **nenhuma**, **parcial**, **todos** quando pertinente. Use dados sintéticos só em teste/proposta, declarados como tal. Valor ausente não vira zero; “Sob consulta” só se for linguagem e regra do produto.

## Trabalho em lote

Uma fila reduz retornos repetidos quando a tarefa exige preparar vários objetos. Especifique apenas os comportamentos necessários ao pedido:

| Transição | Pergunta que a interface deve resolver |
| --- | --- |
| Adicionar/remover | Qual item mudou? A contagem confere? O item em edição ainda existe? |
| Avançar | Qual é o próximo item selecionado? O que já foi preparado fica guardado? |
| Voltar/editar seleção | Quais escolhas e rascunhos permanecem? |
| Revisar | Quais itens estão prontos ou pendentes? É possível corrigir o item certo? |
| Executar | A ação afeta quais itens? A execução é individual, conjunta ou parcial? |
| Falhar parcialmente | Quais itens concluíram? Como retomar sem duplicar os que deram certo? |

O último caso exige suporte real do backend quando houver integração. Uma tela de protótipo pode documentá-lo; não comprova que está implementado. Distinguir “rascunho salvo”, “agendado”, “enviado” e “publicado” conforme os estados reais.

## Estados que mudam a decisão

Não desenhe mecanicamente todos os estados para cada botão. Cubra os que o fluxo pode atingir:

- **Vazio inicial:** o objeto ainda não existe; apresentar a ação útil para começar.
- **Sem resultado:** filtros/busca não encontraram; permitir limpar ou ajustar, preservando o catálogo.
- **Carregando:** comunicar espera na região correta e evitar salto de layout.
- **Erro recuperável:** explicar o que falhou, manter entradas e permitir tentar de novo quando seguro.
- **Indisponível/permissão:** explicar a restrição relevante; não fingir que foi erro de preenchimento.
- **Resultado:** mostrar o que de fato aconteceu e permitir continuar a tarefa, sem telas de celebração obrigatórias.

Preservar valores após erro e associar mensagens aos campos reduz retrabalho. A documentação do [GOV.UK sobre recuperação de erros](https://design-system.service.gov.uk/patterns/validation/) fundamenta esse tratamento. Suas escolhas específicas de validação HTML são próprias daquele sistema; não as aplique automaticamente a qualquer stack.

## Exemplo de aplicação: “vamos fazer a aba de anúncios”

Este exemplo avalia a skill; não é um escopo aprovado para a Lia.

1. Localizar a área atual, o objeto gerenciado, o fluxo documentado, as ações disponíveis e uma tela oficial vizinha.
2. Se o objetivo confirmado for acompanhar anúncios existentes, considerar uma lista/tabela com identidade, situação e dados relevantes, busca/filtros pertinentes e ação principal de criação. Só usar valores e estados sustentados pela fonte.
3. Se o objetivo for compor uma peça, considerar edição com prévia. A composição da tarefa muda; tipografia, navegação, linguagem das ações e tokens continuam coerentes.
4. Conectar entrada, detalhe/edição, resultado e retorno preservando contexto; tratar o estado vazio e o risco principal.
5. Renderizar a tela representativa e exercer o percurso em escopo. Não inventar Meta Ads, orçamento, métricas de performance, automação ou publicação real apenas pelo nome “Anúncios”.

Fontes consultadas em 15/09/2026: base de conhecimento do Brain pessoal; correções da revisão de Stories; documentação GOV.UK acima. As decisões de composição e o exemplo são síntese aplicada, não pesquisa com usuários.
