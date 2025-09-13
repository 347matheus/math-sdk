const symbols = [
  "cenoura", "maçã", "uvas", "ovos", "balde-de-leite",
  "fazendeira", "fazendeiro", "vaca-dourada"
];

// Pagamentos para combinações (3, 4, 5 do mesmo símbolo)
const payouts = {
  "cenoura":     [1, 2, 5],
  "maçã":        [1, 3, 6],
  "uvas":        [1, 4, 8],
  "ovos":        [2, 5, 10],
  "balde-de-leite": [3, 6, 12],
  "fazendeira":  [5, 10, 20],
  "fazendeiro":  [8, 15, 30],
  "vaca-dourada": [0, 0, 0] // especial: não paga no base game
};

function spinReel() {
  return symbols[Math.floor(Math.random() * symbols.length)];
}

function generateSpin() {
  let reels = [];
  for (let i = 0; i < 5; i++) {
    let reel = [];
    for (let j = 0; j < 3; j++) {
      reel.push(spinReel());
    }
    reels.push(reel);
  }
  return reels;
}

function evaluateSpin(reels) {
  let totalWin = 0;
  let bonusTriggered = false;

  // Simples: 10 linhas horizontais (linha 0, 1 e 2 replicadas)
  const paylines = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2],
    [0, 1, 2, 1, 0],
    [2, 1, 0, 1, 2],
    [0, 1, 1, 1, 0],
    [2, 2, 1, 2, 2],
    [1, 0, 1, 2, 1],
    [0, 2, 0, 2, 0],
    [2, 0, 2, 0, 2]
  ];

  for (const line of paylines) {
    const lineSymbols = [];
    for (let r = 0; r < 5; r++) {
      lineSymbols.push(reels[r][line[r]]);
    }

    let count = 1;
    for (let i = 1; i < 5; i++) {
      if (lineSymbols[i] === lineSymbols[0]) {
        count++;
      } else {
        break;
      }
    }

    const symbol = lineSymbols[0];
    if (count >= 3 && payouts[symbol]) {
      totalWin += payouts[symbol][count - 3];
    }

    if (lineSymbols.includes("vaca-dourada")) {
      bonusTriggered = true;
    }
  }

  return { totalWin, bonusTriggered };
}

function playBonus() {
  // Golden Cow Hunt: random multiplier
  const multipliers = [10, 20, 50, 100];
  const picked = multipliers[Math.floor(Math.random() * multipliers.length)];
  const basePrize = 5; // valor fixo ou pode ser variável
  return basePrize * picked;
}

function spin() {
  const reels = generateSpin();
  const result = evaluateSpin(reels);
  let totalWin = result.totalWin;

  let bonusWin = 0;
  if (result.bonusTriggered) {
    bonusWin = playBonus();
    totalWin += bonusWin;
  }

  return {
    reels,
    baseWin: result.totalWin,
    bonusWin: bonusWin,
    totalWin,
    triggeredBonus: result.bonusTriggered
  };
}

module.exports = { spin };

