# Atividade PBL – Aula 17

## Integração Contínua, Qualidade Automatizada, Métricas e Gestão de Defeitos – LocalEats

**Unidade Curricular:** Qualidade de Software
**Prof.:** Luciano Zanuz
**Sistema de referência:** https://local-eats-unisenac.vercel.app/

---

## 🔹 1. Repositório da Atividade

| Item | Descrição |
|------|-----------|
| Nome do repositório | `localeats-ci-laboratorio` |
| Link do repositório | https://github.com/jpmilech/localeats-ci-laboratorio |

### Estrutura de diretórios

```
localeats-ci-laboratorio/
├── order.py                       # Funcionalidade: cálculo do total do pedido
├── requirements.txt               # Dependências (pytest, behave)
├── README.md
├── .gitignore
├── tests/
│   └── test_order.py              # Testes unitários (pytest)
├── features/
│   ├── order_total.feature        # Cenários BDD (Gherkin, pt-BR)
│   └── steps/
│       └── order_total_steps.py   # Implementação dos steps (behave)
├── .github/
│   └── workflows/
│       └── quality.yml            # Pipeline de Integração Contínua
└── aula-17-integracao-continua-qualidade.md
```

---

## 🔹 2. Planejamento da Funcionalidade

| Item | Descrição |
|------|-----------|
| Título da Issue | Implementar cálculo do total do pedido |
| Objetivo da funcionalidade | Calcular o total de um pedido somando o subtotal dos itens (preço × quantidade), aplicando taxa de entrega e desconto, oferecendo frete grátis a partir de um valor mínimo e garantindo que o total nunca seja negativo. |
| Link da Issue | https://github.com/jpmilech/localeats-ci-laboratorio/issues/1 |

---

## 🔹 3. Teste Automatizado

| Item | Descrição |
|------|-----------|
| Tipo de teste | Unitário (pytest) **e** BDD (behave) |
| Objetivo do teste | Garantir que o cálculo do total do pedido está correto em todos os cenários: soma de itens, taxa de entrega, desconto, total não negativo e frete grátis a partir do valor mínimo (inclusive). |
| Link para o arquivo do teste (unitário) | https://github.com/jpmilech/localeats-ci-laboratorio/blob/main/tests/test_order.py |
| Link para o arquivo do teste (BDD) | https://github.com/jpmilech/localeats-ci-laboratorio/blob/main/features/order_total.feature |

### Código do teste (unitário – `tests/test_order.py`)

```python
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


def test_frete_gratis_exatamente_no_limite():
    """Reproduz a Issue #2: pedido igual ao limite deve ter frete grátis.

    Regra: frete grátis a partir de R$ 50,00 (inclusive). Um pedido de
    exatamente R$ 50,00 NÃO pode ser cobrado pela entrega.
    """
    items = [{"price": 50.0, "quantity": 1}]
    total = calculate_order_total(
        items, delivery_fee=8.0, free_delivery_threshold=50.0
    )
    assert total == 50.0
```

### Código do teste (BDD – `features/order_total.feature`)

```gherkin
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

  Cenário: Frete grátis exatamente no limite mínimo
    Dado um pedido com o item "Combo" de preço 50.00 e quantidade 1
    E uma taxa de entrega de 8.00
    E frete grátis a partir de 50.00
    Quando eu calcular o total do pedido
    Então o total deve ser 50.00

  Cenário: Desconto não deixa o total negativo
    Dado um pedido com o item "Suco" de preço 10.00 e quantidade 1
    E um desconto de 999.00
    Quando eu calcular o total do pedido
    Então o total deve ser 0.00
```

---

## 🔹 4. Pipeline de Integração Contínua

| Item | Descrição |
|------|-----------|
| Nome do workflow | Quality CI |
| Evento que dispara a execução | `push` na branch `main` e `pull_request` para a `main` |
| Link para o arquivo do workflow | https://github.com/jpmilech/localeats-ci-laboratorio/blob/main/.github/workflows/quality.yml |
| Link de uma execução do workflow | https://github.com/jpmilech/localeats-ci-laboratorio/actions/runs/28983574205 |

### Código do workflow (`.github/workflows/quality.yml`)

```yaml
name: Quality CI

# Dispara a cada push e a cada pull request na branch main.
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Testes unitários (pytest)
        run: python -m pytest -v

      - name: Testes BDD (behave)
        run: python -m behave
```

---

## 🔹 5. Indicadores de Qualidade

Valores referentes à execução final do pipeline na `main` (após o merge da correção) —
[run 28983574205](https://github.com/jpmilech/localeats-ci-laboratorio/actions/runs/28983574205):

| Indicador | Valor |
|-----------|-------|
| Quantidade de testes executados | 11 (8 testes unitários pytest + 3 cenários BDD behave / 13 steps) |
| Quantidade de testes aprovados | 11 |
| Quantidade de testes com falha | 0 |
| Status final do pipeline | ✅ **SUCCESS** (verde) |

### Análise dos indicadores

O pipeline consolida duas suítes complementares: **8 testes unitários** (pytest), que
validam as regras de cálculo isoladamente, e **3 cenários BDD** (behave, 13 steps), que
validam o comportamento na perspectiva do cliente. Na execução final, **100% dos testes
foram aprovados** e o status do pipeline foi **SUCCESS**.

O valor real do pipeline ficou evidente durante a correção do defeito (seção 6): antes da
correção, a execução do CI ficou **vermelha** ([run 28983513761](https://github.com/jpmilech/localeats-ci-laboratorio/actions/runs/28983513761))
porque o teste de fronteira reprovou (1 falha / 7 aprovados); após a correção, ficou
**verde** ([run 28983545410](https://github.com/jpmilech/localeats-ci-laboratorio/actions/runs/28983545410)).
Isso demonstra, na prática, como o pipeline **impede que uma alteração com defeito seja
integrada à `main`**.

---

## 🔹 6. Registro de Defeito

| Item | Descrição |
|------|-----------|
| Título do defeito | Frete grátis não é aplicado quando o subtotal é exatamente igual ao limite mínimo |
| Severidade | **Média** |
| Link da Issue | https://github.com/jpmilech/localeats-ci-laboratorio/issues/2 |
| Pull Request de correção | https://github.com/jpmilech/localeats-ci-laboratorio/pull/3 |
| Execução do CI com o defeito (🔴) | https://github.com/jpmilech/localeats-ci-laboratorio/actions/runs/28983513761 |
| Execução do CI após correção (🟢) | https://github.com/jpmilech/localeats-ci-laboratorio/actions/runs/28983545410 |

### Descrição

- **Qual foi o defeito?** A regra de negócio prevê frete grátis *a partir* de R$ 50,00 (inclusive), mas um pedido de subtotal exatamente igual a R$ 50,00 continuava sendo cobrado pela taxa de entrega (total R$ 58,00 em vez de R$ 50,00).
- **Como foi identificado?** Um teste automatizado de fronteira (`test_frete_gratis_exatamente_no_limite` e o cenário BDD equivalente) foi adicionado numa Pull Request e reprovou no pipeline de CI (execução vermelha), evidenciando a falha.
- **Como foi corrigido?** A comparação em `order.py` foi alterada de `subtotal > limite` para `subtotal >= limite`. Após o commit da correção, o pipeline voltou a ficar verde e a Pull Request foi mesclada, fechando automaticamente a Issue #2.

---

## 🔁 Fluxo de qualidade demonstrado

> **"Como podemos garantir automaticamente que uma alteração no sistema não introduza novos problemas?"**

1. **Planejamento** → Issue de funcionalidade (#1).
2. **Baseline verde** → `main` com testes automatizados passando no CI.
3. **Defeito registrado** → Issue de bug (#2).
4. **Teste que reproduz o defeito** → Pull Request #3 deixa o pipeline **🔴 vermelho**.
5. **Correção** → commit deixa o pipeline **🟢 verde**.
6. **Integração segura** → merge da PR fecha a Issue; a `main` permanece verde.

O pipeline de Integração Contínua atua como **rede de segurança automática**: nenhuma
alteração é integrada sem que todos os testes (unitários + BDD) passem.
