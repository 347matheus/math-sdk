# 🐄 Cash Cow

**Cash Cow** é um jogo de slot com temática de fazenda, que utiliza um sistema de rodadas normais e um bônus especial chamado **Golden Cow Hunt**. O jogo foi desenvolvido para simular resultados com base em parâmetros ajustáveis, mantendo um RTP (Retorno ao Jogador) em torno de **95%**.

## 🎯 Características do Jogo

- 🎰 5 rolos × 5 linhas (layout de grade)
- 📏 15 linhas de pagamento
- 🍎 Símbolos: Cenoura, Maçã, Uvas, Ovos, Balde de Leite, Fazendeira, Fazendeiro, Vaca Dourada
- 💰 Símbolo especial: Wild
- 🏆 Bônus: **Golden Cow Hunt** com multiplicadores acumulativos

## ⚙️ Estrutura de Pastas

```
cash-cow-math/
├── config/
│   └── config.py              # Base para o GameConfig
├── games/
│   └── cash_cow/
│       ├── game_config.py     # Regras e lógica do jogo
│       └── simulate_game.py   # Simulador para testes de RTP
├── meta.json                  # Descrição para o Stake Engine
└── README.md                  # Este documento
```

## ▶️ Como rodar localmente

```bash
PYTHONPATH="src" python3 games/cash_cow/simulate_game.py
```

> Certifique-se de que está usando Python 3.8 ou superior.

## 📈 RTP

O jogo está calibrado para manter o RTP entre **94% e 96%**, com variações pequenas por rodada.

---

Desenvolvido por Matheus Oliveira • 2025
