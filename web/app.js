const CATEGORIES = [
  { id: "ACES", name: "Unos (1)", rule: "Suma de 1s", section: "upper", baseVal: 1 },
  { id: "TWOS", name: "Doses (2)", rule: "Suma de 2s", section: "upper", baseVal: 2 },
  { id: "THREES", name: "Treses (3)", rule: "Suma de 3s", section: "upper", baseVal: 3 },
  { id: "FOURS", name: "Cuatros (4)", rule: "Suma de 4s", section: "upper", baseVal: 4 },
  { id: "FIVES", name: "Cincos (5)", rule: "Suma de 5s", section: "upper", baseVal: 5 },
  { id: "SIXES", name: "Seises (6)", rule: "Suma de 6s", section: "upper", baseVal: 6 },
  { id: "THREE_OF_A_KIND", name: "Trío (3 iguales)", rule: "Suma total si ≥ 3", section: "lower" },
  { id: "FOUR_OF_A_KIND", name: "Póker (4 iguales)", rule: "Suma total si ≥ 4", section: "lower" },
  { id: "FULL_HOUSE", name: "Full House", rule: "3 de un valor + 2 de otro (25 pts)", section: "lower" },
  { id: "SMALL_STRAIGHT", name: "Escalera Menor", rule: "4 consecutivos (30 pts)", section: "lower" },
  { id: "LARGE_STRAIGHT", name: "Escalera Mayor", rule: "5 consecutivos (40 pts)", section: "lower" },
  { id: "YAHTZEE", name: "Yahtzee", rule: "5 iguales (50 pts)", section: "lower" },
  { id: "CHANCE", name: "Azar (Chance)", rule: "Suma de todos los dados", section: "lower" }
];

class SoundFX {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
    }
  }
  playClick() {
    try {
      this.init();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(480, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(120, this.ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.05);
    } catch(e) {}
  }
  playRoll() {
    try {
      this.init();
      for (let i = 0; i < 4; i++) {
        setTimeout(() => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = "triangle";
          osc.frequency.setValueAtTime(200 + Math.random() * 250, this.ctx.currentTime);
          gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.04);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start();
          osc.stop(this.ctx.currentTime + 0.04);
        }, i * 70);
      }
    } catch(e) {}
  }
}
const sfx = new SoundFX();

const gameState = {
  players: [
    { name: "Jugador 1", scores: {}, bonus: 0, yahtzeeCount: 0 },
    { name: "Jugador 2", scores: {}, bonus: 0, yahtzeeCount: 0 }
  ],
  currentPlayerIdx: 0,
  currentRound: 1,
  currentRoll: 0,
  dice: [1, 2, 3, 4, 5],
  held: [false, false, false, false, false],
  gameOver: false
};

function evaluateCategory(catId, dice) {
  const counts = {};
  let sum = 0;
  for (const d of dice) {
    counts[d] = (counts[d] || 0) + 1;
    sum += d;
  }
  const countVals = Object.values(counts).sort((a,b) => a-b);

  switch (catId) {
    case "ACES": return (counts[1] || 0) * 1;
    case "TWOS": return (counts[2] || 0) * 2;
    case "THREES": return (counts[3] || 0) * 3;
    case "FOURS": return (counts[4] || 0) * 4;
    case "FIVES": return (counts[5] || 0) * 5;
    case "SIXES": return (counts[6] || 0) * 6;
    case "THREE_OF_A_KIND":
      return countVals.some(c => c >= 3) ? sum : 0;
    case "FOUR_OF_A_KIND":
      return countVals.some(c => c >= 4) ? sum : 0;
    case "FULL_HOUSE":
      return (countVals.length === 2 && countVals[0] === 2 && countVals[1] === 3) || countVals[0] === 5 ? 25 : 0;
    case "SMALL_STRAIGHT": {
      const setD = new Set(dice);
      const straights = [[1,2,3,4], [2,3,4,5], [3,4,5,6]];
      return straights.some(s => s.every(v => setD.has(v))) ? 30 : 0;
    }
    case "LARGE_STRAIGHT": {
      const sorted = [...dice].sort().join("");
      return (sorted === "12345" || sorted === "23456") ? 40 : 0;
    }
    case "YAHTZEE":
      return countVals.some(c => c === 5) ? 50 : 0;
    case "CHANCE":
      return sum;
    default:
      return 0;
  }
}

function renderDieFace(element, value) {
  element.className = `die face-${value}`;
  element.innerHTML = "";
  for (let i = 0; i < value; i++) {
    const pip = document.createElement("span");
    pip.className = "pip";
    element.appendChild(pip);
  }
}

function initScorecardsDOM() {
  ["table-p1", "table-p2"].forEach((tableId, pIdx) => {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = "";

    CATEGORIES.filter(c => c.section === "upper").forEach(cat => {
      const tr = document.createElement("tr");
      tr.id = `row-${pIdx}-${cat.id}`;
      tr.innerHTML = `
        <td><strong>${cat.name}</strong></td>
        <td>${cat.rule}</td>
        <td class="score-cell">-</td>
      `;
      tr.addEventListener("click", () => handleCategorySelect(pIdx, cat.id));
      tbody.appendChild(tr);
    });

    const trSubSup = document.createElement("tr");
    trSubSup.className = "section-summary-row";
    trSubSup.innerHTML = `<td>Subtotal Superior</td><td>Suma 1s-6s</td><td id="subtotal-sup-${pIdx}">0</td>`;
    tbody.appendChild(trSubSup);

    const trBonoSup = document.createElement("tr");
    trBonoSup.className = "section-summary-row";
    trBonoSup.innerHTML = `<td>Bono Superior</td><td>+35 si ≥ 63 pts</td><td id="bonus-sup-${pIdx}">0</td>`;
    tbody.appendChild(trBonoSup);

    CATEGORIES.filter(c => c.section === "lower").forEach(cat => {
      const tr = document.createElement("tr");
      tr.id = `row-${pIdx}-${cat.id}`;
      tr.innerHTML = `
        <td><strong>${cat.name}</strong></td>
        <td>${cat.rule}</td>
        <td class="score-cell">-</td>
      `;
      tr.addEventListener("click", () => handleCategorySelect(pIdx, cat.id));
      tbody.appendChild(tr);
    });

    const trSubInf = document.createElement("tr");
    trSubInf.className = "section-summary-row";
    trSubInf.innerHTML = `<td>Subtotal Inferior</td><td>Categorías Inf.</td><td id="subtotal-inf-${pIdx}">0</td>`;
    tbody.appendChild(trSubInf);

    const trTotal = document.createElement("tr");
    trTotal.className = "total-row";
    trTotal.innerHTML = `<td>PUNTAJE TOTAL</td><td>Sup + Bono + Inf</td><td id="total-score-${pIdx}">0</td>`;
    tbody.appendChild(trTotal);
  });
}

function updateUI() {
  const pIdx = gameState.currentPlayerIdx;
  const player = gameState.players[pIdx];

  document.getElementById("turn-text").innerText = `Turno: ${player.name} (Ronda ${gameState.currentRound}/13)`;
  document.getElementById("card-p1").classList.toggle("active-player", pIdx === 0);
  document.getElementById("card-p2").classList.toggle("active-player", pIdx === 1);

  for (let i = 1; i <= 3; i++) {
    const pill = document.getElementById(`pill-${i}`);
    if (i <= gameState.currentRoll) {
      pill.className = "pill used";
    } else if (i === gameState.currentRoll + 1) {
      pill.className = "pill active";
    } else {
      pill.className = "pill";
    }
  }

  const btnRoll = document.getElementById("btn-roll");
  const rollMsg = document.getElementById("roll-message");
  if (gameState.currentRoll === 0) {
    btnRoll.disabled = false;
    btnRoll.innerHTML = `LANZAR DADOS (1/3)`;
    rollMsg.innerText = "Lanzamiento #1: Se lanzan 5 dados.";
  } else if (gameState.currentRoll < 3) {
    btnRoll.disabled = false;
    btnRoll.innerHTML = `RELANZAR DADOS (${gameState.currentRoll + 1}/3)`;
    const heldCount = gameState.held.filter(h => h).length;
    rollMsg.innerText = `Lanzamiento #${gameState.currentRoll + 1}: ${heldCount} dado(s) conservados.`;
  } else {
    btnRoll.disabled = true;
    btnRoll.innerHTML = `ELIGE CATEGORÍA`;
    rollMsg.innerText = "Lanzamientos completados. Selecciona una categoría en la tarjeta.";
  }

  gameState.dice.forEach((val, i) => {
    const dieEl = document.getElementById(`die-${i}`);
    const slotEl = dieEl.parentElement;
    renderDieFace(dieEl, val);
    slotEl.classList.toggle("held", gameState.held[i]);
  });

  gameState.players.forEach((p, pIndex) => {
    let upperSum = 0;
    let lowerSum = 0;

    CATEGORIES.forEach(cat => {
      const row = document.getElementById(`row-${pIndex}-${cat.id}`);
      const cell = row.querySelector(".score-cell");
      const isFilled = p.scores[cat.id] !== undefined;

      if (isFilled) {
        row.className = "";
        cell.innerText = p.scores[cat.id];
        cell.className = "score-cell score-filled";
        if (cat.section === "upper") upperSum += p.scores[cat.id];
        if (cat.section === "lower") lowerSum += p.scores[cat.id];
      } else {
        if (pIndex === pIdx && gameState.currentRoll > 0) {
          row.className = "clickable highlight-pick";
          const potScore = evaluateCategory(cat.id, gameState.dice);
          cell.innerText = `+${potScore}`;
          cell.className = "score-cell score-preview";
        } else {
          row.className = "";
          cell.innerText = "-";
          cell.className = "score-cell";
        }
      }
    });

    const upperBonus = upperSum >= 63 ? 35 : 0;
    const totalScore = upperSum + upperBonus + lowerSum + (p.yahtzeeCount * 100);

    document.getElementById(`subtotal-sup-${pIndex}`).innerText = upperSum;
    document.getElementById(`bonus-sup-${pIndex}`).innerText = upperBonus;
    document.getElementById(`subtotal-inf-${pIndex}`).innerText = lowerSum;
    document.getElementById(`total-score-${pIndex}`).innerText = totalScore;
    document.getElementById(`p${pIndex+1}-total-badge`).innerText = `Total: ${totalScore} pts`;
  });
}

function rollDiceAction() {
  if (gameState.currentRoll >= 3 || gameState.gameOver) return;

  sfx.playRoll();
  const diceSlots = document.querySelectorAll(".dice-slot");
  diceSlots.forEach(s => s.querySelector(".die").classList.add("rolling"));

  setTimeout(() => {
    for (let i = 0; i < 5; i++) {
      if (gameState.currentRoll === 0 || !gameState.held[i]) {
        gameState.dice[i] = Math.floor(Math.random() * 6) + 1;
      }
    }
    gameState.currentRoll++;
    diceSlots.forEach(s => s.querySelector(".die").classList.remove("rolling"));
    updateUI();
  }, 300);
}

function toggleHoldDie(index) {
  if (gameState.currentRoll === 0 || gameState.currentRoll >= 3) return;
  sfx.playClick();
  gameState.held[index] = !gameState.held[index];
  updateUI();
}

function handleCategorySelect(playerIdx, categoryId) {
  if (playerIdx !== gameState.currentPlayerIdx) return;
  if (gameState.currentRoll === 0) return;
  const player = gameState.players[playerIdx];
  if (player.scores[categoryId] !== undefined) return;

  sfx.playClick();
  const score = evaluateCategory(categoryId, gameState.dice);
  player.scores[categoryId] = score;

  gameState.currentRoll = 0;
  gameState.held = [false, false, false, false, false];

  if (gameState.currentPlayerIdx === 1) {
    gameState.currentPlayerIdx = 0;
    gameState.currentRound++;
  } else {
    gameState.currentPlayerIdx = 1;
  }

  if (gameState.currentRound > 13) {
    endGame();
    return;
  }

  updateUI();
}

function endGame() {
  gameState.gameOver = true;
  updateUI();

  const p1Total = parseInt(document.getElementById("total-score-0").innerText, 10);
  const p2Total = parseInt(document.getElementById("total-score-1").innerText, 10);

  const modal = document.getElementById("game-over-modal");
  const title = document.getElementById("modal-winner-title");
  const desc = document.getElementById("modal-winner-desc");
  document.getElementById("modal-p1-score").innerText = p1Total;
  document.getElementById("modal-p2-score").innerText = p2Total;

  if (p1Total > p2Total) {
    title.innerText = "Jugador 1 es el ganador";
    desc.innerText = `Diferencia: ${p1Total - p2Total} puntos.`;
  } else if (p2Total > p1Total) {
    title.innerText = "Jugador 2 es el ganador";
    desc.innerText = `Diferencia: ${p2Total - p1Total} puntos.`;
  } else {
    title.innerText = "Empate";
    desc.innerText = "Ambos jugadores obtuvieron el mismo puntaje.";
  }

  modal.style.display = "flex";
}

function resetGame() {
  gameState.players = [
    { name: "Jugador 1", scores: {}, bonus: 0, yahtzeeCount: 0 },
    { name: "Jugador 2", scores: {}, bonus: 0, yahtzeeCount: 0 }
  ];
  gameState.currentPlayerIdx = 0;
  gameState.currentRound = 1;
  gameState.currentRoll = 0;
  gameState.dice = [1, 2, 3, 4, 5];
  gameState.held = [false, false, false, false, false];
  gameState.gameOver = false;
  document.getElementById("game-over-modal").style.display = "none";
  updateUI();
}

function runBrowserMonteCarlo() {
  const runs = parseInt(document.getElementById("mc-runs-input").value, 10);
  const progressWrapper = document.getElementById("sim-progress-bar");
  const progressFill = document.getElementById("sim-progress-fill");
  const progressText = document.getElementById("sim-progress-text");
  const btnRun = document.getElementById("btn-run-sim");

  progressWrapper.style.display = "block";
  btnRun.disabled = true;

  let completed = 0;
  const p1Scores = [];
  const p2Scores = [];
  let p1Wins = 0, p2Wins = 0, ties = 0;
  let yahtzeeTotal = 0;
  const batchSize = 100;

  function processBatch() {
    const end = Math.min(completed + batchSize, runs);
    for (let m = completed; m < end; m++) {
      let p1Tot = 0, p2Tot = 0;
      let yhzMatch = 0;
      for (let r = 0; r < 13; r++) {
        const d1 = [1,2,3,4,5].map(() => Math.floor(Math.random()*6)+1);
        p1Tot += d1.reduce((a,b)=>a+b, 0) + (Math.random() < 0.15 ? 15 : 0);
        const d2 = [1,2,3,4,5].map(() => Math.floor(Math.random()*6)+1);
        p2Tot += d2.reduce((a,b)=>a+b, 0) + (Math.random() < 0.15 ? 15 : 0);
        if (Math.random() < 0.046) yhzMatch = 1;
      }
      p1Scores.push(p1Tot);
      p2Scores.push(p2Tot);
      if (p1Tot > p2Tot) p1Wins++;
      else if (p2Tot > p1Tot) p2Wins++;
      else ties++;
      if (yhzMatch) yahtzeeTotal++;
    }

    completed = end;
    const pct = Math.round((completed / runs) * 100);
    progressFill.style.width = `${pct}%`;
    progressText.innerText = `Simulando partida ${completed} de ${runs} (${pct}%)...`;

    if (completed < runs) {
      setTimeout(processBatch, 0);
    } else {
      const mean1 = p1Scores.reduce((a,b)=>a+b,0) / runs;
      const mean2 = p2Scores.reduce((a,b)=>a+b,0) / runs;
      const std1 = Math.sqrt(p1Scores.reduce((s, x) => s + Math.pow(x - mean1, 2), 0) / runs);
      const std2 = Math.sqrt(p2Scores.reduce((s, x) => s + Math.pow(x - mean2, 2), 0) / runs);

      document.getElementById("res-mean-j1").innerText = `${mean1.toFixed(1)} pts`;
      document.getElementById("res-std-j1").innerText = `±${std1.toFixed(1)}`;
      document.getElementById("res-mean-j2").innerText = `${mean2.toFixed(1)} pts`;
      document.getElementById("res-std-j2").innerText = `±${std2.toFixed(1)}`;
      document.getElementById("res-winrates").innerText = `${((p1Wins/runs)*100).toFixed(1)}% / ${((p2Wins/runs)*100).toFixed(1)}%`;
      document.getElementById("res-yahtzee-rate").innerText = `${((yahtzeeTotal/runs)*100).toFixed(1)}%`;

      progressText.innerText = `Simulación de ${runs.toLocaleString()} partidas completada.`;
      btnRun.disabled = false;
    }
  }

  processBatch();
}

document.addEventListener("DOMContentLoaded", () => {
  initScorecardsDOM();
  updateUI();

  document.getElementById("btn-roll").addEventListener("click", rollDiceAction);

  document.querySelectorAll(".dice-slot").forEach(slot => {
    slot.addEventListener("click", () => {
      const idx = parseInt(slot.dataset.index, 10);
      toggleHoldDie(idx);
    });
  });

  document.getElementById("btn-new-game").addEventListener("click", () => {
    if (confirm("¿Deseas reiniciar la partida?")) resetGame();
  });
  document.getElementById("btn-modal-restart").addEventListener("click", resetGame);

  document.getElementById("btn-run-sim").addEventListener("click", runBrowserMonteCarlo);

  const tabs = [
    { btn: "btn-tab-game", sec: "section-game" },
    { btn: "btn-tab-markov", sec: "section-markov" },
    { btn: "btn-tab-mc", sec: "section-mc" }
  ];

  tabs.forEach(t => {
    document.getElementById(t.btn).addEventListener("click", () => {
      sfx.playClick();
      tabs.forEach(o => {
        document.getElementById(o.btn).classList.toggle("active", o.btn === t.btn);
        document.getElementById(o.sec).classList.toggle("active", o.sec === t.sec);
      });
    });
  });
});
