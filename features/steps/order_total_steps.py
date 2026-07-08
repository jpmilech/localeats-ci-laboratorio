"""Steps BDD (behave) para a funcionalidade de cálculo do total do pedido."""

from behave import given, when, then

from order import calculate_order_total


@given('um pedido com o item "{nome}" de preço {preco:f} e quantidade {qtd:d}')
def step_pedido_com_item(context, nome, preco, qtd):
    context.items = [{"price": preco, "quantity": qtd}]
    context.delivery_fee = 0.0
    context.discount = 0.0
    context.free_delivery_threshold = None


@given('uma taxa de entrega de {valor:f}')
def step_taxa_de_entrega(context, valor):
    context.delivery_fee = valor


@given('um desconto de {valor:f}')
def step_desconto(context, valor):
    context.discount = valor


@given('frete grátis a partir de {valor:f}')
def step_frete_gratis(context, valor):
    context.free_delivery_threshold = valor


@when('eu calcular o total do pedido')
def step_calcular_total(context):
    context.total = calculate_order_total(
        context.items,
        delivery_fee=context.delivery_fee,
        discount=context.discount,
        free_delivery_threshold=context.free_delivery_threshold,
    )


@then('o total deve ser {esperado:f}')
def step_verificar_total(context, esperado):
    assert context.total == esperado, (
        f"Esperado {esperado}, obtido {context.total}"
    )
