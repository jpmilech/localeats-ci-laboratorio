"""Cálculo do total de um pedido no LocalEats.

Funcionalidade: calcular o valor total de um pedido a partir dos itens,
aplicando taxa de entrega, desconto e frete grátis acima de um valor mínimo.
"""


def calculate_order_total(items, delivery_fee=0.0, discount=0.0,
                          free_delivery_threshold=None):
    """Calcula o total de um pedido.

    Args:
        items: lista de dicionários com as chaves "price" e "quantity".
        delivery_fee: taxa de entrega aplicada ao pedido.
        discount: valor de desconto a ser subtraído do total.
        free_delivery_threshold: se informado, quando o subtotal atingir
            (ou ultrapassar) esse valor a taxa de entrega é zerada.

    Returns:
        O total do pedido, arredondado em 2 casas e nunca negativo.
    """
    subtotal = sum(item["price"] * item["quantity"] for item in items)

    fee = delivery_fee
    if free_delivery_threshold is not None and subtotal >= free_delivery_threshold:
        # Frete grátis a partir do valor mínimo (inclusive).
        fee = 0.0

    total = subtotal + fee - discount
    # O total nunca pode ser negativo.
    return round(max(total, 0.0), 2)
