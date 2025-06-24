# Teste de Integração: Marketplace (Painel Web ↔ Bot Discord ↔ API)

## 1. Adicionar item pelo painel web
- Acesse `/marketplace` no painel.
- Preencha nome, preço e descrição e clique em "Adicionar".
- Verifique se o item aparece na lista de itens à venda.
- No Discord, use o comando `!mercado` e confira se o item aparece.
- Faça uma requisição GET `/marketplace` na API e confira se o item está listado.

## 2. Comprar item pelo painel web
- Clique em "Comprar" em um item à venda no painel.
- Verifique se o item some da lista de itens à venda no painel.
- No Discord, use `!mercado` e confira se o item não aparece mais.
- Verifique se o saldo do comprador e vendedor foi atualizado corretamente (se aplicável).
- Faça uma requisição GET `/marketplace` na API e confira se o item está marcado como vendido.

## 3. Adicionar item pelo comando do bot
- No Discord, use `!vender <preco> <nome do item>`.
- Verifique se o item aparece no painel web e na API.

## 4. Comprar item pelo comando do bot
- No Discord, use `!comprar <id do item>`.
- Verifique se o item some do painel web e da API.
- Verifique atualização de saldo e histórico.

## 5. Teste de concorrência
- Tente comprar o mesmo item ao mesmo tempo pelo painel e pelo Discord.
- O sistema deve permitir apenas uma compra e retornar erro para a segunda tentativa.

## 6. Teste de erros
- Tente comprar item inexistente ou já vendido (painel e bot).
- O sistema deve retornar mensagem de erro adequada.

---

Repita o fluxo para outros módulos (ex: skill tree, conquistas, economia) adaptando os endpoints e comandos.

**Se algum passo falhar, registre o erro para correção!**
