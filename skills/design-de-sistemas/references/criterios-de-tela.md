# Critérios de tela pronta

Adotado por Bernardo em 13/10/2026, no Virapátio. Ele percebeu a diferença entre os dois jeitos de trabalhar:
- **"Faz todas as telas":** a entrega saiu genérica e mal pensada. Os campos vinham do banco de dados.
- **Tela por tela:** cadastro de carro, contato, ficha, Radar e Revisar procuras ficaram muito melhores.

Pedido dele: "pode demorar um pouco mais, mas a entrega com certeza vai ser melhor". Vale para todo sistema e app dele.

## Regra de trabalho
- **Uma parte por vez** (tela, bloco ou passo do fluxo, como no método por partes de `../../contexto/criar-telas.md`, 21/10). Um pedido de "todas as telas" vira uma fila, e cada parte passa por este roteiro.
- **Agentes, workflows e sessões paralelas recebem o pacote do Brain** (lista em `../../contexto/criar-telas.md`, "Pacote do Brain para agentes e workflows"), que inclui este arquivo, e devolvem a ficha preenchida. O integrador confere a ficha de cada tela antes de juntar.
- **Ajuste pequeno já decidido** (trocar rótulo, alinhar) não passa pelo roteiro inteiro: confere só o critério atingido.

## Antes de desenhar
1. **Cena de uso.** Em uma frase: quem usa, onde, com que pressa e quantas vezes por dia.
   - Ex.: "vendedor no pátio, celular numa mão, cliente do lado, 15 vezes por dia".
   - A cena decide o tamanho dos botões, a densidade e o que vem primeiro.
2. **Tarefa antes dos campos.** Responda "o que a pessoa quer resolver aqui em 30 segundos?".
   - O obrigatório para essa tarefa vem primeiro. O resto vai para "Mais detalhes", recolhido.
   - Nunca desenhar a partir da tabela do banco.
3. **Referência real.** Olhe como um app bom resolve a mesma tarefa (OLX, Webmotors, WhatsApp, Nubank, iFood…) e o repertório do Brain.
   - Copie o padrão que o usuário já conhece antes de inventar.

## Ao construir
4. **Escolher em vez de digitar.** Botões, chips, seletor que rola, sugestões e valores já preenchidos pelo contexto (último usado, carro aberto, hoje).
5. **Poucos toques.** Conte os toques da tarefa principal: a meta é até cerca de 5, sem rolar dentro de janela. Se passar, simplifique antes de seguir.
6. **Uma ação principal por tela,** sempre no mesmo lugar.
   - O nome é verbo + coisa ("Salvar carro"), seguindo o guia de textos do projeto.
   - Ações raras ou perigosas ficam em "Mais opções".
7. **Onde estou e o que faço agora.** A tela precisa ter:
   - título que diz para que ela serve;
   - próximo passo visível;
   - depois de cada ação, um aviso do que mudou e do que fazer agora (o aviso some sozinho e não cobre botão);
   - tela vazia que ensina, com o botão da primeira ação.
8. **Volume e tropeços reais.** Teste com:
   - 0, 1 e 50 itens (lista longa pede busca e filtro);
   - texto longo e dado faltando;
   - internet que falha, clique duplo e engano.
   - Engano se resolve com "Desfazer" quando possível, em vez de janela de confirmação.

## Antes de mostrar a Bernardo
9. **Teste do dia a dia.** Faça a tarefa como o usuário da cena, no celular e no computador, com dado realista (ex.: carro de verdade com foto).
   - Pergunte o que irrita na décima vez do dia. Isso vira atalho, valor padrão ou filtro.
10. **Ficha de nota.** Com o print na frente, dê nota 0, 1 ou 2 em cada critério de 1 a 9.
    - Tudo abaixo de 2 é corrigido antes de mostrar.
    - Na escolha, Bernardo recebe as 2 ou 3 opções da parte, cada uma com o link, uma linha do que muda e a recomendação com o motivo. Depois de aplicada, recebe a tela, o link e uma linha "o que melhorei além do pedido".
    - A ficha fica no registro do projeto, não no chat.

## O que já se mostrou errado (não repetir)
- Formulário com 17 campos numa janela comprida; foto só depois de salvar; ano digitado.
- Painel vazio ocupando metade da tela ("escolha um contato").
- Jargão do sistema na tela: operação, recibo, versão, reconferência.
- Aviso parado por cima de botão.
- Lista de 50 itens sem busca.
- Detalhe técnico aberto sozinho (privacidade).
