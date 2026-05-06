# BFS/DFS Router Pitch

Projeto para demonstrar DFS com pilha em uma malha de roteadores inspirada em Fortaleza.

## Cenarios

- `preventive_monitoring_success`: mostra a rede conectada e validada antes de um incidente.
- `fiber_theft_outage`: simula o roubo de fibra em `2025-08-14` e destaca os bairros isolados.
- `fiber_theft_recovered`: mostra a malha restabelecida em `2025-08-15` apos o reparo.

## Como executar

```bash
python main.py --plain
```

Para executar apenas um cenario:

```bash
python main.py --plain --scenario fiber_theft_outage
```

## O que o pitch mostra

- DFS partindo da central para verificar quais roteadores continuam alcancaveis.
- Cenarios de sucesso, falha por roubo de fibra e recuperacao posterior.
- Monitor de bairros vulneraveis com cobertura, risco medio e status.
