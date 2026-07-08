"""Testes unitários (pytest) da funcionalidade de cálculo do total do pedido."""

from order import calculate_order_total


def test_subtotal_de_um_item():
    items = [{"price": 25.0, "quantity": 2}]
    assert calculate_order_total(items) == 50.0


def test_subtotal_de_varios_itens():
    items = [
        {"price": 25.0, "quantity": 2},   # 50.00
        {"price": 12.5, "quantity": 1},   # 12.50
    ]
    assert calculate_order_total(items) == 62.5


def test_soma_taxa_de_entrega():
    items = [{"price": 30.0, "quantity": 1}]
    assert calculate_order_total(items, delivery_fee=8.0) == 38.0


def test_aplica_desconto():
    items = [{"price": 30.0, "quantity": 1}]
    assert calculate_order_total(items, discount=5.0) == 25.0


def test_total_nunca_e_negativo():
    items = [{"price": 10.0, "quantity": 1}]
    assert calculate_order_total(items, discount=999.0) == 0.0


def test_frete_gratis_acima_do_limite():
    items = [{"price": 60.0, "quantity": 1}]
    total = calculate_order_total(
        items, delivery_fee=8.0, free_delivery_threshold=50.0
    )
    assert total == 60.0


def test_frete_cobrado_abaixo_do_limite():
    items = [{"price": 49.9, "quantity": 1}]
    total = calculate_order_total(
        items, delivery_fee=8.0, free_delivery_threshold=50.0
    )
    assert total == 57.9
