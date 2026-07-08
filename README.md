# LocalEats — Laboratório de CI e Qualidade

Repositório da atividade PBL – Aula 17 (Qualidade de Software – Unisenac-RS).
Demonstra um fluxo de qualidade automatizado com testes, Integração Contínua
(GitHub Actions) e gestão de defeitos via GitHub Issues.

Sistema de referência: https://local-eats-unisenac.vercel.app/

## Funcionalidade

Cálculo do total de um pedido (`order.py`): soma os itens, aplica taxa de
entrega e desconto, garante frete grátis a partir de um valor mínimo e nunca
retorna total negativo.

## Como rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

pytest -v      # testes unitários
behave         # testes BDD
```

## Estrutura

```
localeats-ci-laboratorio/
├── order.py                     # funcionalidade
├── requirements.txt
├── tests/
│   └── test_order.py            # testes unitários (pytest)
├── features/
│   ├── order_total.feature      # cenários BDD (Gherkin, pt-BR)
│   └── steps/
│       └── order_total_steps.py # implementação dos steps (behave)
├── .github/
│   └── workflows/
│       └── quality.yml          # pipeline de CI
└── aula-17-integracao-continua-qualidade.md   # entrega
```

## CI

O workflow **Quality CI** roda a cada `push` e `pull_request` na `main`,
executando os testes unitários (pytest) e de comportamento (behave).
