# language: pt
Funcionalidade: Cálculo do total do pedido
  Como cliente do LocalEats
  Quero que o total do meu pedido seja calculado corretamente
  Para saber quanto vou pagar, incluindo entrega e descontos

  Cenário: Somar itens e taxa de entrega
    Dado um pedido com o item "Pizza" de preço 40.00 e quantidade 1
    E uma taxa de entrega de 8.00
    Quando eu calcular o total do pedido
    Então o total deve ser 48.00

  Cenário: Desconto não deixa o total negativo
    Dado um pedido com o item "Suco" de preço 10.00 e quantidade 1
    E um desconto de 999.00
    Quando eu calcular o total do pedido
    Então o total deve ser 0.00
