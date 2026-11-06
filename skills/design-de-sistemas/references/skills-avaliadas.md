# Skills externas avaliadas — 15/09/2026

Consulta pontual e teste exploratório solicitados por Bernardo. Não executar as três skills em toda tarefa. Elas complementam critérios locais; não conhecem automaticamente as escolhas ou regras de negócio da Lia.

## Candidatas e decisão de uso

| Fonte inspecionada | Contribuição útil | Limite encontrado | Encaminhamento |
| --- | --- | --- | --- |
| [Interface Design](https://github.com/Dammyjay93/interface-design/blob/2f9be3206855bcb2d1d0af262c8bae25cba6658d/.claude/skills/interface-design/SKILL.md) | Composição, densidade, hierarquia, reutilização de componentes e tokens | Tem prescrições de cor do menu, profundidade e exploração por componente que podem conflitar com a identidade e a agilidade da Lia | Repertório para direção/composição quando necessário; preservar escolhas do projeto |
| [Impeccable](https://github.com/pbakaus/impeccable/blob/0a4e72a254f3b175c95b36b82e5f2e60fa63f116/.agents/skills/impeccable/SKILL.md) | Modo Operate distingue trabalho administrativo de marketing; layout e harden orientam agrupamento e estados adversos | Workflow completo inclui launcher/binário e documentos próprios; contém regras estéticas prescritivas | Candidata principal para revisão pontual, desde que operação e escopo sejam respeitados |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/15de38fb70bc80ae9276fa7703b48ae861a672e6/.claude/skills/ui-ux-pro-max/SKILL.md) | Busca local de orientações de UX por tema e stack | Busca depende da formulação; geração de sistema visual pode introduzir outra identidade se aplicada sem contexto | Consulta pontual de comportamento/stack; não regenerar o design system aprovado |

Essa é uma avaliação de adequação ao caso, não ranking comprovado de qualidade gerada por modelos.

## Evidência da avaliação

Cópias selecionadas foram guardadas fora do catálogo ativo, com commits, SHA-256 e licenças, em [sources.json](/Users/bernardo/Documents/Codex/2026-09-15/avaliacao-skills-design/sources.json). Não foram instalados os pacotes completos, hooks ou dependências. O launcher/detector do Impeccable não foi executado.

A busca Python do UI/UX Pro Max foi executada localmente. Houve resultados pertinentes para arrasto, retorno, resultado vazio e overflow. “carousel keyboard selection” trouxe itens genéricos; a reformulação “carousel drag controls” encontrou arrasto e controle de rotação. Portanto, validar assunto e plataforma do resultado antes de aplicá-lo. A saída da busca não é autoridade normativa.

O [piloto visual local](/Users/bernardo/Documents/Codex/2026-09-15/avaliacao-skills-design/piloto.html) apresenta três composições do mesmo problema, aplicadas pelo mesmo autor com as orientações consultadas. Ele usa fotos de exemplo repetidas para volume. Foram inspecionadas as três versões no desktop 1440×900 e exercitados seleção, avanço, retorno, erro recuperável, 0/1/12 fotos, texto longo, arrasto, troca de layout e sequência de Tab/Enter. Resultados em [browser-checks.json](/Users/bernardo/Documents/Codex/2026-09-15/avaliacao-skills-design/browser-checks.json).

O piloto detectou um contraste inadequado no hover do controle ativo e uma distribuição vertical excessiva na primeira renderização; ambos foram ajustados. Isso ilustra o valor da verificação do resultado. Não comprova que uma skill específica evitou o problema nem que houve ganho de produtividade.

Não houve teste independente por modelo, aplicação no Figma oficial, mobile, modo escuro, backend ou publicação. O piloto não mede qualidade global da skill nem implementa o pedido da conversa principal.

## Cuidado com regras absolutas

Não converter heurística em norma. A Interface Design descreve 44×44 como WCAG e menciona 40 como mínimo; a documentação oficial distingue [mínimo AA de 24×24 com exceções](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) do [critério aprimorado AAA de 44×44 com exceções](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html). Uma equipe pode adotar 44px por conforto, mas a justificativa precisa ser correta.

Também não usar “sem rolagem horizontal” de um checklist para proibir todo carrossel ou tabela com overflow intencional. Diferenciar transbordamento acidental da página, interação de coleção e requisitos de acessibilidade aplicáveis.

## Uso futuro

Quando o usuário pedir uma dessas skills pelo nome, carregar sua versão realmente disponível e seguir as instruções pertinentes, respeitando as instruções superiores e a autorização atual. Esta avaliação não dispensa setup obrigatório de um pacote invocado. Se a versão mudar, verificar apenas o trecho do workflow/capacidade que será usado.

Novas instalações globais ou mudanças em regras de outros projetos não decorrem desta lista. A camada local conserva decisões e critérios; o pacote externo entra pela necessidade específica.
